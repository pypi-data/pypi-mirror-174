from gantry.logger.event_builder import _build_data_link
from gantry.logger.constants import BatchType, UploadFileType


def test_build_data_link(datadir):
    csv_file = datadir / "feedback.csv"
    data_link = _build_data_link(
        application="test_app",
        version=0,
        environment="dev",
        feedback_id=["feedback_id"],
        feedbacks=["test_float", "test_int"],
        filepath=str(csv_file),
    )

    assert data_link.application == "test_app"
    assert data_link.version == "0"
    assert data_link.file_type == UploadFileType.CSV_WITH_HEADERS
    assert data_link.batch_type == BatchType.FEEDBACK
    assert data_link.tags["env"].val == "dev"
    assert data_link.feedback_id["feedback_id"].ref == 0
    assert data_link.feedback["test_float"].ref == 1
    assert data_link.feedback["test_int"].ref == 2
