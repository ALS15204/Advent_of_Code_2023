from pathlib import Path
from typing import List


SCRIPT_DIR = Path(__file__).parent
INPUT_FILE_PATH = SCRIPT_DIR / "input.dat"


def line_str_to_int_sequence(line: str) -> List[int]:
    return [int(x) for x in line.split()]


def construct_diffrence_lists(int_sequence: List[int]) -> List[List[int]]:
    diffrence_lists = []
    last_diffrence_list = int_sequence
    while len(last_diffrence_list) > 0 and sum(last_diffrence_list) != 0:
        diffrence_list = []
        for num, next_num in zip(last_diffrence_list[:-1], last_diffrence_list[1:]):
            diffrence_list.append(next_num - num)
        diffrence_lists.append(diffrence_list)
        last_diffrence_list = diffrence_list
    return diffrence_lists


def find_next_number(int_sequence: List[int]) -> int:
    diffrence_lists = construct_diffrence_lists(int_sequence)
    return int_sequence[-1] + sum([diff_list[-1] for diff_list in diffrence_lists])


def main():
    with open(INPUT_FILE_PATH) as f:
        input_lines = [line.strip("\n") for line in f.readlines()]
    sequences = [line_str_to_int_sequence(line) for line in input_lines]
    answer_1 = sum([find_next_number(sequence) for sequence in sequences])
    print(f"Answer to Part 1: {answer_1}")

    answer_2 = sum([find_next_number(sequence[::-1]) for sequence in sequences])
    print(f"Answer to Part 2: {answer_2}")


if __name__ == "__main__":
    main()