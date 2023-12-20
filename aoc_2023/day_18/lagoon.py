from pathlib import Path
from typing import List, Tuple

from aoc_2023.day_10.maze import sum_tuple_list_by_element

SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "example.dat"


DIRECTIONS_TO_COORDINATES = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}
EMPTY = "."
DUGGED = "#"


def dig_map(
        trench_map: List[List[str]], starting_point: Tuple[int, int], direction: Tuple[int, int], step: int
        ) -> List[List[str]]:
    end_point = (starting_point[0] + direction[0] * step, starting_point[1] + direction[1] * step)
    drow, dcol = 0, 0
    if end_point[0] < 0:
        drow = abs(end_point[0])
        trench_map = [[EMPTY] * len(trench_map[0])] * drow + trench_map
    elif end_point[0] >= len(trench_map):
        for _ in range(end_point[0] - len(trench_map) + 1):
            trench_map.extend([[EMPTY] * len(trench_map[0])])
    if end_point[1] < 0:
        dcol = abs(end_point[1])
        trench_map = [[EMPTY] * dcol + line for line in trench_map]
    elif end_point[1] >= len(trench_map[0]):
        trench_map = [line + [EMPTY] * (end_point[1] - len(trench_map[0]) + 1) for line in trench_map]
    starting_point = (starting_point[0] + drow, starting_point[1] + dcol)
    end_point = (end_point[0] + drow, end_point[1] + dcol)
    row, col = starting_point
    for i in range(1, step + 1, 1):
        drow, dcol = direction
        trench_map[row + drow * i][col + dcol * i] = DUGGED
    return trench_map, end_point


def count_border(row: List[str]) -> int:
    count = 0
    previous_block = row[0]
    if previous_block == DUGGED:
        count += 1
    for i in range(len(row) - 1):
        current_block = row[i + 1]
        if current_block == DUGGED and previous_block == EMPTY:
            count += 1
        previous_block = current_block
    return count


def main():
    with INPUT_DATA.open("r") as fp:
        data = fp.read().splitlines()
    trench_map = [[DUGGED]]
    starting_point = (0, 0)
    for data_line in data:
        direction, step, _ = data_line.split()
        step = int(step)
        trench_map, starting_point = dig_map(trench_map, starting_point, DIRECTIONS_TO_COORDINATES[direction], step)
    boundaries = {(row, col) for row, line in enumerate(trench_map) for col, char in enumerate(line) if char == DUGGED}
    n_tile = 0
    for row in range(len(trench_map)):
        for col in range(len(trench_map[0])):
            if (row, col) in boundaries:
                n_tile += 1
            else:
                row_to_point = trench_map[row][:col + 1]
                col_to_point = [line[col] for line in trench_map[:row + 1]]
                if count_border(row_to_point) % 2 == 1:
                    # trench_map[row][col] = DUGGED
                    n_tile += 1
    # with open(SCRIPT_DIR / "lagoon_map.dat", "w") as fp:
    #     for line in trench_map:
    #         fp.write("".join(line) + "\n")
    print(f"Answer to Part 1: {n_tile}")
    pass


if __name__ == "__main__":
    main()