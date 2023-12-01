from pytest import mark
from aoc_2023.utils.digits import replace_letters_by_digits, find_first_digit, get_code_in_line


@mark.parametrize("text, expected", [
    ("twoneerwt094r", "2w1neerwt094r"), 
    ("oneightfdca032", "1n8ightfdca032"), 
    ("oneightfouroneight", "1n8ight4our1n8ight")
    ]
)
def test_replace_letters_by_digits(text, expected):
    assert replace_letters_by_digits(text) == expected


@mark.parametrize("text, expected", [
    ("three28jxdmlqfmc619eightwol", "2"), 
    ("nineone81mkltdkfgxtsevenfive", "8"), 
    ("1two743six", "1")
    ]
)
def test_find_first_digit(text, expected):
    assert find_first_digit(text) == expected


@mark.parametrize("text, expected", [
    ("three28jxdmlqfmc619eightwol", ("2", "6")), 
    ("nineone81mkltdkfgxtsevenfive", ("8", "5")), 
    ("1two743six", ("1", "6"))
    ]
)
def test_get_code_in_line_without_spelling_out(text, expected):
    assert get_code_in_line(text) == expected


@mark.parametrize("text, expected", [
    ("three28jxdmlqfmc619eightwol", ("3", "2")), 
    ("nineone81mkltdkfgxtsevenfive", ("9", "5")), 
    ("1two743six", ("1", "6"))
    ]
)
def test_get_code_in_line_without_spelling_out(text, expected):
    assert get_code_in_line(text, spelled_out_digits=True) == expected