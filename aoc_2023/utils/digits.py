import re
from typing import Tuple


DIGIT_REGEX = re.compile(r"\d")
LETTERS_TO_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def replace_letters_by_digits(text: str) -> str:
    new_text = " " * len(text)
    for letter, digit in LETTERS_TO_DIGITS.items():
        letter_regex = re.compile(letter)
        digit_positions = [m.start() for m in letter_regex.finditer(text) if m]
        for pos in digit_positions:
            new_text = new_text[:pos] + str(digit) + new_text[pos + 1:]
    text = "".join(c if not new_c.strip() else new_c for c, new_c in zip(text, new_text))
    return text


def find_first_digit(text: str) -> str:
    try:
        return DIGIT_REGEX.search(text).group()
    except AttributeError:
        return None


def get_code_in_line(line_text: str, spelled_out_digits: bool=False) -> Tuple[str, str]:
    if spelled_out_digits:
        line_text = replace_letters_by_digits(line_text)
    first_digit = find_first_digit(line_text)
    if first_digit is None:
        return None, None
    last_digit = find_first_digit(line_text[::-1])
    return first_digit, last_digit