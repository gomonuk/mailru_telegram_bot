import pytest

from src.reverse_polish_notation import (
    bad_brackets_error,
    create_rpn,
    exec_rpn,
    string_normalization,
)


@pytest.mark.parametrize(
    argnames="tests",
    argvalues=[
        (
            "3  + 7",
            (["3", "+", "7"], None),
        ),
        (
            "3 * 1 + 2 * 3",
            (["3", "*", "1", "+", "2", "*", "3"], None),
        ),
        (
            "3 * (1 + 2) * 3",
            (["3", "*", "(", "1", "+", "2", ")", "*", "3"], None),
        ),
        (
            "3 * (1 + 2 * 3",
            (["3", "*", "(", "1", "+", "2", "*", "3"], bad_brackets_error),
        ),
    ],
)
def test_string_normalization(tests):
    input_str, expected = tests
    assert string_normalization(input_str) == expected


@pytest.mark.parametrize(
    argnames="tests",
    argvalues=[
        (["3", "+", "7"], [3, 7, "+"]),
        (["3", "*", "1", "+", "2", "*", "3"], [3, 1, "*", 2, 3, "*", "+"]),
        (["3", "*", "(", "1", "+", "2", ")", "*", "3"], [3, 1, 2, "+", "*", 3, "*"]),
    ],
)
def test_create_rpn(tests):
    input_str, expected = tests
    assert create_rpn(input_str) == expected


@pytest.mark.parametrize(
    argnames="tests",
    argvalues=[
        ([3, 7, "+"], 10),
        ([3, 1, "*", 2, 3, "*", "+"], 9),
        ([3, 1, 2, "+", "*", 3, "*"], 27),
    ],
)
def test_exec_rpn(tests):
    input_str, expected = tests
    assert exec_rpn(input_str) == expected
