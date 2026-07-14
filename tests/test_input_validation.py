import pytest

from car.models import Step
from car.validation import is_valid_range, ERROR_MESSAGES


@pytest.mark.parametrize("step,ans,expected", [
    (Step.CAR_TYPE, 0, False),
    (Step.CAR_TYPE, 1, True),
    (Step.CAR_TYPE, 3, True),
    (Step.CAR_TYPE, 4, False),
    (Step.ENGINE, -1, False),
    (Step.ENGINE, 0, True),
    (Step.ENGINE, 4, True),
    (Step.ENGINE, 5, False),
    (Step.BRAKE, 0, True),
    (Step.BRAKE, 3, True),
    (Step.BRAKE, 4, False),
    (Step.STEERING, 0, True),
    (Step.STEERING, 2, True),
    (Step.STEERING, 3, False),
    (Step.FINAL, 0, True),
    (Step.FINAL, 2, True),
    (Step.FINAL, 3, False),
])
def test_is_valid_range(step, ans, expected):
    assert is_valid_range(step, ans) == expected


def test_error_messages_exist_for_every_step():
    for step in Step:
        assert step in ERROR_MESSAGES
        assert ERROR_MESSAGES[step].startswith("ERROR ::")
