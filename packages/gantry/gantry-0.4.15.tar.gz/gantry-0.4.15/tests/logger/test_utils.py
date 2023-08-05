import json
import pytest
import pandas as pd
from io import StringIO

from gantry.exceptions import GantryBatchCreationException, GantryLoggingException  # noqa
from gantry.logger.utils import _build_batch_iterator, _is_empty, _is_not_empty, _log_exception


@pytest.mark.parametrize(
    ["test_obj", "expected_result"],
    [
        (pd.DataFrame(), True),
        (pd.DataFrame.from_dict({"A": [200, 201]}), False),
        ([1, 2, 3], False),
        ([], True),
        (None, True),
    ],
)
def test_is_empty(test_obj, expected_result):
    assert _is_empty(test_obj) is expected_result


@pytest.mark.parametrize(
    ["test_obj", "expected_result"],
    [
        (pd.DataFrame(), False),
        (pd.DataFrame.from_dict({"A": [200, 201]}), True),
        ([1, 2, 3], True),
        ([], False),
        (None, False),
    ],
)
def test_is_not_empty(test_obj, expected_result):
    assert _is_not_empty(test_obj) is expected_result


def test_log_exception():
    try:
        _log_exception(lambda: exec("raise(GantryLoggingException())"))()
    except Exception as e:
        pytest.fail(f"_log_exception() failed due to raising {e}")
    with pytest.raises(GantryBatchCreationException):
        _log_exception(lambda: exec("raise(GantryBatchCreationException())"))()
    try:
        _log_exception(lambda: exec("raise(Exception())"))()
    except Exception as e:
        pytest.fail(f"_log_exception() failed due to raising {e}")


def test_build_batch_iterator():
    event_list = [{1: 1}, {2: 2}, {3: 3}, {4: 4}, {5: 5}]
    # We should only have 3 batches created from the list.
    batch_iter = _build_batch_iterator(event_list, 2)
    iters = 0
    for _ in batch_iter:
        iters += 1
    assert iters == 3

    # We should still have all 5 lines in the file
    batch_iter = _build_batch_iterator(event_list, 2)
    result = "".join([part.decode("utf-8") for part in batch_iter])
    file = StringIO(result)

    for line in file.readlines():
        json.loads(line)

    file.seek(0)
    assert len(file.readlines()) == 5
