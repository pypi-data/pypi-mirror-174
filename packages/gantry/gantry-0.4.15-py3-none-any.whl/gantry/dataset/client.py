import uuid
from typing import Dict, List, Optional

from gantry.api_client import APIClient
from gantry.dataset.gantry_dataset import GantryDataset


class GantryDatasetClient:
    def __init__(
        self,
        api_client: APIClient,
        email: str,
        bucket_name: Optional[str] = None,
        aws_region: Optional[str] = None,
        workspace: str = ".",
    ):
        self._api_client = api_client
        self.email = email
        self.bucket_name = bucket_name
        self.aws_region = aws_region
        self.workspace = workspace

    def create_dataset(self, name: str, model_id: Optional[uuid.UUID] = None) -> GantryDataset:
        """
        Create dataset

        Args:
            name (str): dataset name
            model_id (Optional[uuid.UUID], optional): gantry model id which will be used to set
                dataset schema if provided.

        Returns:
            GantryDataset
        """
        data = {
            "name": name,
            "email": self.email,
        }
        if model_id:
            data["model_id"] = str(model_id)

        if self.bucket_name and self.aws_region:
            data.update(
                {
                    "bucket_name": self.bucket_name,
                    "aws_region": self.aws_region,
                }
            )
        elif not (not self.bucket_name and not self.aws_region):
            raise NotImplementedError(
                "Both bucket name and region need to be set if you want\
                 to use your own bucket."
            )

        res = self._api_client.request("POST", "/api/v1/datasets", json=data, raise_for_status=True)

        return GantryDataset(
            api_client=self._api_client,
            user_email=self.email,
            dataset_name=res["data"]["name"],
            dataset_id=res["data"]["id"],
            bucket_name=res["data"]["bucket_name"],
            aws_region=res["data"]["aws_region"],
            dataset_s3_prefix=f"{res['data']['organization_id']}/{res['data']['s3_prefix']}",
            workspace=self.workspace,
        )

    def get_dataset(self, name: str) -> GantryDataset:
        """
        Get dataset object

        Args:
            name (str): dataset name

        Returns:
            GantryDataset
        """
        res = self._api_client.request("GET", f"/api/v1/datasets/{name}", raise_for_status=True)

        return GantryDataset(
            api_client=self._api_client,
            user_email=self.email,
            dataset_name=res["data"]["name"],
            dataset_id=res["data"]["id"],
            bucket_name=res["data"]["bucket_name"],
            aws_region=res["data"]["aws_region"],
            dataset_s3_prefix=f"{res['data']['organization_id']}/{res['data']['s3_prefix']}",
            workspace=self.workspace,
        )

    def list_dataset_commits(self, name: str) -> List[Dict[str, str]]:
        """
        Show dataset commit history

        Args:
            name (str): dataset name

        Returns:
            list of commit info
        """
        dataset_id = self.get_dataset(name)._dataset_id
        res = self._api_client.request(
            "GET", f"/api/v1/datasets/{dataset_id}/commits", raise_for_status=True
        )

        return res["data"]

    def list_datasets(self) -> List[Dict[str, str]]:
        """
        List datasets

        Returns:
            List of dataset information
        """
        res = self._api_client.request("GET", "/api/v1/datasets", raise_for_status=True)

        return res["data"]
