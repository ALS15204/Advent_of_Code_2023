from pathlib import Path
from typing import List, Tuple
from scipy.optimize import curve_fit


SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "input.dat"

START = "S"
FARM = "."
STONE = "#"
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


def find_start_coordinate(map: List[List[str]]) -> Tuple[int, int]:
    for i, row in enumerate(map):
        for j, col in enumerate(row):
            if col == START:
                return i, j

def fit(x, a, b):
    return a * x ** b


def main():
    with open(INPUT_DATA) as f:
        data = f.read().splitlines()

    start = find_start_coordinate(data)

    total_step = 64
    n_step = 0
    points = [start]
    while n_step < total_step:
        next_points = set()
        for point in points:
            for direction in DIRECTIONS:
                next_point = (point[0] + direction[0], point[1] + direction[1])
                if 0 <= next_point[0] < len(data) and 0 <= next_point[1] < len(data[0]) and data[next_point[0]][next_point[1]] in {FARM, START}:
                    next_points.add(next_point)
        points = next_points
        n_step += 1
    print(f"Answer to part 1: {len(points)}")

    test_step = 500
    total_step = 26501365
    n_step = 0
    points = [start]
    x = []
    y = []
    while n_step < test_step:
        next_points = set()
        for point in points:
            for direction in DIRECTIONS:
                next_point = (point[0] + direction[0], point[1] + direction[1])
                if data[next_point[0] % len(data)][next_point[1] % len(data[0])] in {FARM, START}:
                    next_points.add(next_point)
        points = next_points
        n_step += 1
        x.append(n_step)
        y.append(len(points))
    popt, pcov = curve_fit(fit, x, y)[0]
    print(f"Answer to part 2: {int(popt * total_step ** pcov)}")


if __name__ == "__main__":
    main()
