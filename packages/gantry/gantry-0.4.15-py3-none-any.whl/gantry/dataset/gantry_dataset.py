import json
import logging
import os
import shutil
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from gantry.api_client import APIClient
from gantry.dataset import constants
from gantry.exceptions import GantryRequestException
from gantry.utils import (
    download_file_from_url,
    get_files_checksum,
    parse_s3_path,
    upload_file_to_url,
)

logger = logging.getLogger(__name__)

BATCH_SIZE = 5


@dataclass
class DatasetFileInfo:
    file_name: str
    url: str
    version_id: Optional[str] = None
    sha256: Optional[str] = None

    def to_jsonl(self):
        if not self.file_name or not self.url or not self.version_id or not self.sha256:
            raise ValueError(
                f"Failed to create file info jsonl: {json.dumps(asdict(self))}. \
                    Incomplete dataset file info line! "
            )

        return f"{json.dumps(asdict(self))}\n"


class GantryDataset:
    def __init__(
        self,
        api_client: APIClient,
        dataset_name: str,
        user_email: str,
        dataset_id: uuid.UUID,
        bucket_name: str,
        aws_region: str,
        dataset_s3_prefix: str,
        workspace: str,
    ):
        self.dataset_name = dataset_name
        self.user_email = user_email
        self.workspace = workspace
        self._api_client = api_client
        self._dataset_id = dataset_id
        self._bucket_name = bucket_name
        self._dataset_s3_prefix = dataset_s3_prefix
        self._aws_region = aws_region

    def list_commits(self) -> List[Dict[str, str]]:
        """
        Get dataset commits history

        Returns:
            List[Dict[str, str]]: dataset commits sorted from latest to earlist.
        """
        response = self._api_client.request(
            "GET", f"/api/v1/datasets/{self._dataset_id}/commits", raise_for_status=True
        )
        return response["data"]

    def get_diff(self) -> Dict[str, List[str]]:
        """
        Get local changes which hasn't been committed
        Return:
            {
                "new_files": List[str],
                "modified_files": List[str],
                "deleted_files": List[str],
            }
        """
        diff = self._get_diff()
        return {
            constants.NEW_FILES: [f.file_name for f in diff[constants.NEW_FILES]],
            constants.MODIFIED_FILES: [f.file_name for f in diff[constants.MODIFIED_FILES]],
            constants.DELETED_FILES: [f.file_name for f in diff[constants.DELETED_FILES]],
        }

    def create_commit(self, message: str) -> Dict[str, str]:
        """
        This method will compute the difference between the current commit and the local directory,
        upload new files and modified files to dataset repo. After that we will update
        .gantry_artifact.jsonl with the latest dataset info and create a new commit. HEAD file
        will also be updated using the latest commit information.

        Args:
            message (str): commit message, can't be empty
        Returns:
            Commit info
        """
        diff = self._get_diff()

        if (
            not diff[constants.NEW_FILES]
            and not diff[constants.MODIFIED_FILES]
            and not diff[constants.DELETED_FILES]
        ):
            logger.warning("No local changes to commit!")
            return self._get_current_commit()
        diff[constants.NEW_FILES] = self._upload_files(diff[constants.NEW_FILES])
        diff[constants.MODIFIED_FILES] = self._upload_files(diff[constants.MODIFIED_FILES])

        self._backup_file(constants.DATASET_MANIFEST_FILE)
        self._update_manifest_file(diff)

        result = self._upload_files(
            [
                DatasetFileInfo(
                    file_name=constants.DATASET_MANIFEST_FILE,
                    url=self._get_s3_url(constants.DATASET_MANIFEST_FILE),
                )
            ]
        )
        version_id = result[0].version_id
        try:
            resp = self._api_client.request(
                "POST",
                f"/api/v1/datasets/{self._dataset_id}/commits",
                json={
                    "message": message,
                    "metadata_s3_file_version": version_id,
                    "parent_commit_id": self._get_current_commit()["id"],
                    "email": self.user_email,
                },
                raise_for_status=True,
            )
            os.remove(
                self._get_file_path(f"{constants.DATASET_MANIFEST_FILE}{constants.BACKUP_SUFFIX}")
            )
        except GantryRequestException as e:
            self._recover_file(constants.DATASET_MANIFEST_FILE)
            raise e

        commit_info = resp["data"]
        self._update_head(commit_info)

        return commit_info

    def sync(self, commit_id: Optional[str] = None) -> Dict[str, str]:
        """
        Sync local dataset folder based on a commit id. If commit_id was not provided, will sync
        based on the latest commit.

        Args:
            commit_id (str, optional): target commit id. Defaults to None.
        Returns:
            commit info
        """
        target_commit = (
            self.get_commit(commit_id=commit_id) if commit_id else self.get_latest_commit()
        )

        version_id = target_commit[constants.METADATA_S3_FILE_VERSION]

        self._download_files(
            [
                DatasetFileInfo(
                    file_name=constants.DATASET_MANIFEST_FILE,
                    url=self._get_s3_url(constants.DATASET_MANIFEST_FILE),
                    version_id=version_id,
                )
            ]
        )

        diff = self._get_diff(return_local_info=False)
        self._download_files(diff[constants.MODIFIED_FILES])  # Overwrite modified files
        self._download_files(diff[constants.DELETED_FILES])  # redownload deleted files

        # delete new added files
        for f in diff[constants.NEW_FILES]:
            os.remove(self._get_file_path(f.file_name))

        self._update_head(target_commit)

        return target_commit

    def get_commit(self, commit_id: str) -> Dict[str, str]:
        """
        Get commit details

        Args:
            commit_id (str): commit id
        Returns:
            Commit information
        """
        resp = self._api_client.request(
            "GET", f"/api/v1/datasets/{self._dataset_id}/commits/{commit_id}", raise_for_status=True
        )
        return resp["data"]

    def get_latest_commit(self) -> Dict[str, str]:
        """
        Get latest commit details

        Returns:
            Commit information
        """
        resp = self._api_client.request(
            "GET", f"/api/v1/datasets/{self._dataset_id}/commits", raise_for_status=True
        )
        return resp["data"][0]  # return latest commit

    def _update_manifest_file(self, diff: Dict[str, List[DatasetFileInfo]]):
        new_files = dict([(f.file_name, f) for f in diff[constants.NEW_FILES]])
        modified_files = dict([(f.file_name, f) for f in diff[constants.MODIFIED_FILES]])
        deleted_files = dict([(f.file_name, f) for f in diff[constants.DELETED_FILES]])

        with open(
            self._get_file_path(f"{constants.DATASET_MANIFEST_FILE}{constants.NEW_SUFFIX}"), "w"
        ) as new_gantry_manifest:
            with open(
                self._get_file_path(constants.DATASET_MANIFEST_FILE), "r"
            ) as cur_gantry_manifest:
                for line in cur_gantry_manifest:
                    cur_file_info = json.loads(line)
                    cur_file_name = cur_file_info[constants.FILE_NAME]

                    if cur_file_name in modified_files:  # update modified files
                        new_gantry_manifest.write(modified_files[cur_file_name].to_jsonl())
                    elif cur_file_name in deleted_files:  # remove deleted files
                        continue
                    else:  # keep unchanged files
                        new_gantry_manifest.write(line)

            for _, file_info in new_files.items():
                new_gantry_manifest.write(file_info.to_jsonl())  # add new added files

        os.replace(
            self._get_file_path(f"{constants.DATASET_MANIFEST_FILE}{constants.NEW_SUFFIX}"),
            self._get_file_path(constants.DATASET_MANIFEST_FILE),
        )

    def _get_diff(self, return_local_info=True):
        """
        Generate local diff.

        Args:
            return_local_info (bool): if true return local file info for modiflied files else
            return file info in dataset repo

        Returns:
            {
                "new_files": List[DatasetFileInfo],
                "modified_files": List[DatasetFileInfo],
                "deleted_files": List[DatasetFileInfo],
            }
        """
        repo_diff = defaultdict(list)

        commit_snapshot = {}
        with open(self._get_file_path(constants.DATASET_MANIFEST_FILE)) as cur_gantry_manifest:
            for line in cur_gantry_manifest:
                file_info = json.loads(line)
                commit_snapshot[file_info[constants.FILE_NAME]] = file_info

        local_files = get_files_checksum(Path(self.workspace) / self.dataset_name)

        # TODO:// Simplify the following logic to make it easier to maintain
        for file_name, checksum in local_files.items():
            if file_name.startswith(constants.GANTRY_FOLDER):  # skip .dataset_metadata folder
                continue
            elif file_name not in commit_snapshot:  # new added file
                repo_diff[constants.NEW_FILES].append(
                    DatasetFileInfo(
                        file_name=file_name,
                        url=self._get_s3_url(file_name),
                        sha256=checksum,
                    )
                )
            elif checksum != commit_snapshot[file_name].get(
                constants.SHA256
            ):  # if file_name in current_snapshot --> check if it has been modified
                if return_local_info:
                    repo_diff[constants.MODIFIED_FILES].append(
                        DatasetFileInfo(
                            file_name=file_name,
                            url=self._get_s3_url(file_name),
                            sha256=checksum,
                        )
                    )
                else:
                    repo_diff[constants.MODIFIED_FILES].append(
                        DatasetFileInfo(
                            file_name=file_name,
                            url=commit_snapshot[file_name][constants.URL],
                            version_id=commit_snapshot[file_name][constants.VERSION_ID],
                            sha256=commit_snapshot[file_name][constants.SHA256],
                        )
                    )

        for file_name in commit_snapshot:
            if file_name not in local_files:
                repo_diff[constants.DELETED_FILES].append(
                    DatasetFileInfo(
                        file_name=file_name,
                        url=commit_snapshot[file_name][constants.URL],
                        sha256=commit_snapshot[file_name][constants.SHA256],
                        version_id=commit_snapshot[file_name][constants.VERSION_ID],
                    )
                )
        return repo_diff

    def _get_file_path(self, file_name: str) -> str:
        return os.path.join(self.workspace, self.dataset_name, file_name)

    def _get_s3_url(self, file_name: str) -> str:
        return f"s3://{self._bucket_name}/{self._dataset_s3_prefix}/{self.dataset_name}/{file_name}"

    def _get_obj_key(self, s3_url: str) -> str:
        _, obj_key = parse_s3_path(s3_url)
        return obj_key

    def _update_head(self, commit_info: Dict[str, str]):
        with open(self._get_file_path(constants.DATASET_HEAD_FILE), "w") as f:
            json.dump(commit_info, f)

    def _get_current_commit(self) -> Dict[str, str]:
        with open(self._get_file_path(constants.DATASET_HEAD_FILE), "r") as f:
            return json.load(f)

    def _backup_file(self, file_path: str):
        # make a copy of the original file
        shutil.copyfile(
            self._get_file_path(file_path),
            self._get_file_path(f"{file_path}{constants.BACKUP_SUFFIX}"),
        )

    def _recover_file(self, file_path: str):
        # recover the file from a backup copy
        os.replace(
            self._get_file_path(f"{file_path}{constants.BACKUP_SUFFIX}"),
            self._get_file_path(file_path),
        )

    def _download_files(self, file_list: List[DatasetFileInfo]):
        """
        download file to the specific path

        Args:
            file_list (List[DatasetFileInfo]):
        """
        for i in range(0, len(file_list), BATCH_SIZE):
            batch = file_list[i : i + BATCH_SIZE]
            resp = self._api_client.request(
                "POST",
                f"/api/v1/datasets/{self._dataset_id}/presign/getobject",
                json={
                    "obj_infos": [
                        {
                            constants.OBJ_KEY: self._get_obj_key(item.url),
                            constants.VERSION_ID: item.version_id,
                        }
                        for item in batch
                    ],
                },
                raise_for_status=True,
            )
            presigned_urls = resp["data"]

            for item in batch:
                local_path = self._get_file_path(item.file_name)
                presigned_url = presigned_urls.get(self._get_obj_key(item.url))
                download_file_from_url(presigned_url=presigned_url, local_path=Path(local_path))

    def _upload_files(self, file_list: List[DatasetFileInfo]):
        """
        download file to the specific path

        Args:
            file_list (List[DatasetFileInfo]):
        Returns:
            List[DatasetFileInfo]
        """
        for i in range(0, len(file_list), BATCH_SIZE):
            batch = file_list[i : i + BATCH_SIZE]
            resp = self._api_client.request(
                "POST",
                f"/api/v1/datasets/{self._dataset_id}/presign/putobject",
                json={"obj_keys": [self._get_obj_key(f.url) for f in batch]},
                raise_for_status=True,
            )
            presigned_urls = resp["data"]

            for item in batch:
                local_path = self._get_file_path(item.file_name)
                presigned_url = presigned_urls.get(self._get_obj_key(item.url))
                version_id = upload_file_to_url(
                    presigned_url=presigned_url, local_path=Path(local_path)
                )
                item.version_id = version_id
                logger.info(f"successfully upload: {item.file_name}")

        return file_list
