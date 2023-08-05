import json
from io import StringIO
from pathlib import Path

import pytest
import responses
from responses import matchers

from gantry.api_client import APIClient
from gantry.dataset.constants import DELETED_FILES, MODIFIED_FILES, NEW_FILES
from gantry.dataset.gantry_dataset import DatasetFileInfo, GantryDataset
from gantry.exceptions import GantryException

from .conftest import (
    AWS_REGION,
    BUCKET_NAME,
    COMMIT_MSG,
    CONF_OBJ_KEY,
    CSV_OBJ_KEY,
    DATASET_ID,
    DATASET_NAME,
    HOST,
    IMG_OBJ_KEY,
    MANIFEST_OBJ_KEY,
    MANIFEST_VERSION_ID,
    README_OBJ_KEY,
    S3_PREFIX,
    USER_EMAIL,
)


@pytest.fixture
def test_api_client():
    return APIClient(origin=HOST)


@pytest.fixture(scope="function")
def gantry_dataset_obj(test_api_client, datadir):
    return GantryDataset(
        api_client=test_api_client,
        dataset_name=DATASET_NAME,
        user_email=USER_EMAIL,
        dataset_id=DATASET_ID,
        bucket_name=BUCKET_NAME,
        aws_region=AWS_REGION,
        dataset_s3_prefix=S3_PREFIX,
        workspace=datadir,
    )


def test_list_commits(gantry_dataset_obj, commit_history):
    """
    Test get dataset commits
    """
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets/{DATASET_ID}/commits",
            json={
                "response": "ok",
                "data": commit_history,
            },
            headers={"Content-Type": "application/json"},
        )
        commits = gantry_dataset_obj.list_commits()
        assert len(commits) == 2


def test_get_commit(gantry_dataset_obj, commit_history):
    """
    Test get commit information
    """
    expected_commit = commit_history[1]
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets/{DATASET_ID}/commits/{expected_commit['id']}",
            json={
                "response": "ok",
                "data": expected_commit,
            },
            headers={"Content-Type": "application/json"},
        )
        commit = gantry_dataset_obj.get_commit(expected_commit["id"])
        assert commit == expected_commit


def test_get_latest_commit(gantry_dataset_obj, commit_history):
    """
    Test get latest commit
    """
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets/{DATASET_ID}/commits",
            json={
                "response": "ok",
                "data": commit_history,
            },
            headers={"Content-Type": "application/json"},
        )
        latest_commit = gantry_dataset_obj.get_latest_commit()
        assert latest_commit["id"] == "8ee0f6d5-c84c-473a-931a-5148b2e704d7"
        assert latest_commit["is_latest_commit"]


def test_get_diff(gantry_dataset_obj):
    """
    Test get local edit diff
    """
    # overwrite the dataset name
    gantry_dataset_obj.dataset_name = "show_diff_dataset"

    diff = gantry_dataset_obj.get_diff()

    assert set(diff[NEW_FILES]) == {"artifacts/kitten.png", "tabular_manifests/feedback.csv"}
    assert diff[MODIFIED_FILES] == ["dataset_config.yaml"]
    assert diff[DELETED_FILES] == ["README.md"]


def setup_resp_for_create_commit(
    datadir, resp, create_commit_resp_json, create_commit_status_code=200
):
    resp.add(
        resp.POST,
        f"{HOST}/api/v1/datasets/{DATASET_ID}/presign/putobject",
        json={
            "response": "ok",
            "data": {
                MANIFEST_OBJ_KEY: f"{HOST}/fake_presigned_url",
                CONF_OBJ_KEY: f"{HOST}/fake_presigned_url",
                README_OBJ_KEY: f"{HOST}/fake_presigned_url",
                IMG_OBJ_KEY: f"{HOST}/fake_presigned_url",
                CSV_OBJ_KEY: f"{HOST}/fake_presigned_url",
            },
        },
        headers={"Content-Type": "application/json"},
    )

    resp.add(
        resp.PUT,
        f"{HOST}/fake_presigned_url",
        json={"response": "ok"},
        headers={"Content-Type": "application/json", "x-amz-version-id": MANIFEST_VERSION_ID},
    )

    with open(datadir / f"{DATASET_NAME}/.dataset_metadata/HEAD") as f:
        old_commit = json.load(f)

    resp.add(
        resp.POST,
        f"{HOST}/api/v1/datasets/{DATASET_ID}/commits",
        json=create_commit_resp_json,
        headers={"Content-Type": "application/json"},
        status=create_commit_status_code,
        match=[
            matchers.json_params_matcher(
                {
                    "message": COMMIT_MSG,
                    "metadata_s3_file_version": MANIFEST_VERSION_ID,
                    "parent_commit_id": old_commit["id"],
                    "email": USER_EMAIL,
                }
            )
        ],
    )


def test_create_commit(datadir, gantry_dataset_obj, commit_history):
    """
    Test create commit succeed
    """
    with responses.RequestsMock() as resp:
        setup_resp_for_create_commit(datadir, resp, {"response": "ok", "data": commit_history[0]})

        gantry_dataset_obj.create_commit(COMMIT_MSG)

        diff = gantry_dataset_obj.get_diff()

        # verify no diff after a successful commit
        assert not diff[NEW_FILES]
        assert not diff[MODIFIED_FILES]
        assert not diff[DELETED_FILES]

        with open(datadir / f"{DATASET_NAME}/.dataset_metadata/HEAD") as f:
            assert json.load(f) == commit_history[0]  # verify HEAD has been updated


def test_create_commit_failure(datadir, gantry_dataset_obj):
    """
    Test create commit failure, in this case all upload will finish successfully but the create
    commit call will fail. This will happen during a race condition when another user committed a
    change and the local copy out of date.
    """
    with responses.RequestsMock() as resp:
        setup_resp_for_create_commit(
            datadir, resp, {"response": "error", "error": "Parent commit out of date!"}, 400
        )

        with pytest.raises(GantryException):
            gantry_dataset_obj.create_commit(COMMIT_MSG)

        diff = gantry_dataset_obj.get_diff()

        # since commit failed the local diff will be the same
        assert set(diff[NEW_FILES]) == {"artifacts/kitten.png", "tabular_manifests/feedback.csv"}
        assert diff[MODIFIED_FILES] == ["dataset_config.yaml"]
        assert diff[DELETED_FILES] == ["README.md"]


def test_create_commit_nochange(datadir, gantry_dataset_obj):
    """
    Test create commit without any local change
    """
    gantry_dataset_obj.dataset_name = "unittest_dataset"
    with open(datadir / "unittest_dataset/.dataset_metadata/HEAD") as f:
        old_commit = json.load(f)

    new_commit = gantry_dataset_obj.create_commit("new commit")
    assert old_commit == new_commit


def create_mock_manifest(commit_history):
    gantry_manifest = StringIO()
    config_file_info = {
        "file_name": "dataset_config.yaml",
        "url": f"s3://test-bucket/{CONF_OBJ_KEY}",
        "sha256": "unmatched_sha256",
        "version_id": "random_vid_for_config",
    }

    gantry_manifest.write(f"{json.dumps(config_file_info)}\n")

    readme_file_info = {
        "file_name": "README.md",
        "url": f"s3://test-bucket/{README_OBJ_KEY}",
        "sha256": "unmatched_sha256",
        "version_id": "random_vid_for_readme",
    }

    gantry_manifest.write(f"{json.dumps(readme_file_info)}\n")
    gantry_manifest.seek(0)
    commit_json = commit_history[1]

    return gantry_manifest, commit_json


@pytest.mark.parametrize("commit_id", [None, "eb2e7242-3340-4edf-8366-90d4fce897ce"])
def test_sync_dataset(commit_id, datadir, gantry_dataset_obj, commit_history):
    """
    Test sync local data set
    1. To latest commit
    2. To a specific commit
    """
    manifest_file, commit_json = create_mock_manifest(commit_history)

    gantry_dataset_obj.dataset_name = "show_diff_dataset"

    with responses.RequestsMock() as resp:
        if commit_id is not None:
            resp.add(
                resp.GET,
                f"{HOST}/api/v1/datasets/{DATASET_ID}/commits/{commit_id}",
                json={
                    "response": "ok",
                    "data": commit_json,
                },
                headers={"Content-Type": "application/json"},
            )
        else:
            resp.add(
                resp.GET,
                f"{HOST}/api/v1/datasets/{DATASET_ID}/commits",
                json={
                    "response": "ok",
                    "data": [commit_json],
                },
                headers={"Content-Type": "application/json"},
            )

        resp.add(
            resp.POST,
            f"{HOST}/api/v1/datasets/{DATASET_ID}/presign/getobject",
            json={
                "response": "ok",
                "data": {
                    MANIFEST_OBJ_KEY: f"{HOST}/fake_manifest",
                    CONF_OBJ_KEY: f"{HOST}/fake_presigned_url",
                    README_OBJ_KEY: f"{HOST}/fake_presigned_url",
                },
            },
            headers={"Content-Type": "application/json"},
        )

        req_kwargs = {
            "stream": True,
        }
        resp.add(
            resp.GET,
            f"{HOST}/fake_presigned_url",
            body="fake_response",
            match=[matchers.request_kwargs_matcher(req_kwargs)],
        )

        resp.add(
            resp.GET,
            f"{HOST}/fake_manifest",
            body=manifest_file.read(),
            match=[matchers.request_kwargs_matcher(req_kwargs)],
        )
        commit = gantry_dataset_obj.sync(commit_id)
        assert commit == commit_json
        with open(datadir / "show_diff_dataset/dataset_config.yaml", "r") as f:
            assert f.read() == "fake_response"

        with open(datadir / "show_diff_dataset/README.md", "r") as f:
            assert f.read() == "fake_response"

        with open(datadir / "show_diff_dataset/.dataset_metadata/HEAD") as f:
            assert json.load(f) == commit_json

        assert not any(Path(datadir / "show_diff_dataset/tabular_manifests").iterdir())
        assert not any(Path(datadir / "show_diff_dataset/artifacts").iterdir())


def test_to_jsonl():
    file_info = DatasetFileInfo(
        file_name="test_file",
        url="s3://test-bucket/key",
        version_id="version_id",
        sha256="mock_sha256",
    )
    assert (
        file_info.to_jsonl()
        == '{"file_name": "test_file", "url": "s3://test-bucket/key", "version_id": "version_id", \
"sha256": "mock_sha256"}\n'
    )


@pytest.mark.parametrize(
    ["file_name", "url", "version_id", "sha256"],
    [
        (None, "s3://test-bucket/key", "version_id", "mock_sha256"),
        ("test_file", None, "version_id", "mock_sha256"),
        ("test_file", "s3://test-bucket/key", None, "mock_sha256"),
        ("test_file", "s3://test-bucket/key", "version_id", None),
    ],
)
def test_to_jsonl_value_error(file_name, url, version_id, sha256):
    file_info = DatasetFileInfo(
        file_name=file_name,
        url=url,
        version_id=version_id,
        sha256=sha256,
    )
    with pytest.raises(ValueError):
        file_info.to_jsonl()
