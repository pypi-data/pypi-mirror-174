import pytest
import responses
from gantry.api_client import APIClient
from gantry.dataset.client import GantryDatasetClient
from .conftest import (
    HOST,
    USER_EMAIL,
    BUCKET_NAME,
    AWS_REGION,
    DATASET_NAME,
    DATASET_ID,
)


@pytest.fixture
def test_api_client():
    return APIClient(origin=HOST)


@pytest.fixture
def test_client(test_api_client):
    return GantryDatasetClient(
        api_client=test_api_client,
        email=USER_EMAIL,
        bucket_name=BUCKET_NAME,
        aws_region=AWS_REGION,
    )


def test_create_dataset(test_client, test_dataset):
    """
    Test create dataset
    """
    with responses.RequestsMock() as resp:
        resp.add(
            resp.POST,
            f"{HOST}/api/v1/datasets",
            json={
                "response": "ok",
                "data": test_dataset,
            },
            headers={"Content-Type": "application/json"},
        )
        dataset = test_client.create_dataset(DATASET_NAME)
        assert dataset.user_email == USER_EMAIL
        assert dataset._dataset_id == DATASET_ID
        assert dataset.dataset_name == DATASET_NAME
        assert dataset.workspace == "."


def test_get_dataset(test_client, test_dataset):
    """
    Test get dataset
    """
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets/{DATASET_NAME}",
            json={
                "response": "ok",
                "data": test_dataset,
            },
            headers={"Content-Type": "application/json"},
        )
        dataset = test_client.get_dataset(DATASET_NAME)
        assert dataset.user_email == USER_EMAIL
        assert dataset._dataset_id == DATASET_ID
        assert dataset.dataset_name == DATASET_NAME
        assert dataset.workspace == "."


def test_dataset_commits(test_client, test_dataset, commit_history):
    """
    Test get dataset commits
    """
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets/{DATASET_NAME}",
            json={
                "response": "ok",
                "data": test_dataset,
            },
            headers={"Content-Type": "application/json"},
        )
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets/{DATASET_ID}/commits",
            json={
                "response": "ok",
                "data": commit_history,
            },
            headers={"Content-Type": "application/json"},
        )
        commits = test_client.list_dataset_commits(DATASET_NAME)
        assert len(commits) == 2


def test_list_datasets(test_client, test_dataset):
    """
    List datasets
    """
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/datasets",
            json={
                "response": "ok",
                "data": [test_dataset],
            },
            headers={"Content-Type": "application/json"},
        )
        datasets = test_client.list_datasets()
        assert len(datasets) == 1
