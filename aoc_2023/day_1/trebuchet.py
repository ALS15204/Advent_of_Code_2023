from pathlib import Path

from aoc_2023.utils.digits import get_code_in_line

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_DIR / "input.dat"


def main():
    with open(INPUT_DATA, "r") as f:
        data = [line.strip("\n") for line in f.readlines()]

    # PART 1: Consider pure digits
    sum_part_1 = 0
    for line in data:
        first_digit, last_digit = get_code_in_line(line)
        if first_digit is None:
            continue
        sum_part_1 += int(f"{first_digit}{last_digit}")
    print(f"Answer to part 1: {sum_part_1}")

    # PART 2: Consider digits in words
    sum_part_2 = 0
    for line in data:
        first_digit, last_digit = get_code_in_line(line, spelled_out_digits=True)
        if first_digit is None:
            continue
        sum_part_2 += int(f"{first_digit}{last_digit}")
    print(f"Answer to part 2: {sum_part_2}")


if __name__ == "__main__":
    main()