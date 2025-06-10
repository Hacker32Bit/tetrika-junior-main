import pytest
from solution import strict, sum_two


def test_sum_two_valid():
    assert sum_two(1, 2) == 3


def test_sum_two_invalid_type():
    with pytest.raises(TypeError, match="Argument 'b' must be of type int"):
        sum_two(1, 2.4)


def test_sum_two_return_type_violation():
    @strict
    def fake_sum(a: int, b: int) -> str:
        return a + b  # Returns int instead of str

    with pytest.raises(TypeError, match="Return value must be of type str"):
        fake_sum(1, 2)
