from pathlib import Path
from typing import List, Tuple

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "example.dat"

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


def get_adjacent_locs(loc: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [(loc[0] + d[0], loc[1] + d[1]) for d in DIRECTIONS]


def loc_in_bounds(loc: Tuple[int, int], data: List[List[str]]):
    return 0 <= loc[0] < len(data) and 0 <= loc[1] < len(data[0])


def find_shortest_path(data: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]):
    path = {}
    current_loc = start
    while current_loc != end:
        path.add(current_loc)
        next_loc_candidates = {loc for loc in get_adjacent_locs(current_loc) if loc not in path if loc_in_bounds(loc, data)}
        next_loc = min(next_loc_candidates, key=lambda loc: data[loc[0]][loc[1]])
        current_loc = next_loc

    pass


def main():
    with open(INPUT_DATA) as f:
        data = [[int(c) for c in line ] for line in f.read().splitlines()]
    grid = Grid(matrix=data)
    start = grid.node(0, 0)
    end = grid.node(len(data) - 1, len(data[0]) - 1)
    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)
    sum([p.weight for p in path])
    print(data)


if __name__ == "__main__":
    main()