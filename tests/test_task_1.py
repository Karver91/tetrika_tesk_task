import pytest

from task_1.solution import sum_two


def test_strict_with_positional_args():
    a = 1
    b = 3
    assert sum_two(a, b) == a + b


def test_strict_with_named_args():
    a = 1
    b = 3
    assert sum_two(a=a, b=b) == a + b


def test_strict_multiple_args():
    a, b, c = 1, 2, 3
    with pytest.raises(TypeError):
        sum_two(a=a, b=b, c=c)


def test_strict_type_is_not_valid():
    a = 1
    b = 2.4
    with pytest.raises(TypeError):
        sum_two(1, 2.4)