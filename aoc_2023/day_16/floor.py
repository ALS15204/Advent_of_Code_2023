from pathlib import Path
from typing import List, Tuple

SCRPIT_DIR = Path(__file__).parent
INPUT_DATA = "input.dat"

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
EMPTY = "."
IN_MIRROR_TO_OUT = {
    (UP, "|"): {UP},
    (DOWN, "|"): {DOWN},
    (LEFT, "-"): {LEFT},
    (RIGHT, "-"): {RIGHT},
    (UP, "/"): {RIGHT},
    (DOWN, "/"): {LEFT},
    (LEFT, "/"): {DOWN},
    (RIGHT, "/"): {UP},
    (UP, "\\"): {LEFT},
    (DOWN, "\\"): {RIGHT},
    (LEFT, "\\"): {UP},
    (RIGHT, "\\"): {DOWN},
    (UP, "-"): {LEFT, RIGHT},
    (DOWN, "-"): {LEFT, RIGHT},
    (LEFT, "|"): {UP, DOWN},
    (RIGHT, "|"): {UP, DOWN},
}
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def find_beam_map(data: List[str], initial_location: Tuple[int, int], direction: Tuple[int, int]) -> List[str]:
    beam_map = [[EMPTY] * len(line) for line in data]
    path_continue = True
    location_to_directions = {initial_location: {direction}}
    path = {}
    while path_continue:
        previous_path = path.copy()
        for location, directions in location_to_directions.items():
            path[location] = directions
            if location[0] < 0 or location[0] >= len(data) or location[1] < 0 or location[1] >= len(data[0]):
                continue
            beam_map[location[0]][location[1]] = "#"
        new_location_to_directions = {}
        for location, directions in location_to_directions.items():
            for direction in directions:
                new_location = (location[0] + direction[0], location[1] + direction[1])
                if new_location[0] < 0 or new_location[0] >= len(data) or new_location[1] < 0 or new_location[1] >= len(data[0]):
                    continue
                if new_location not in new_location_to_directions:
                    new_location_to_directions[new_location] = set()
                mirror = data[new_location[0]][new_location[1]]
                if mirror == EMPTY:
                    new_location_to_directions[new_location].add(direction)
                else:
                    new_location_to_directions[new_location].update(IN_MIRROR_TO_OUT[(direction, mirror)]) 
        if path == previous_path:
            for location in new_location_to_directions:
                beam_map[location[0]][location[1]] = "#"
            path_continue = False
        else:
            location_to_directions = new_location_to_directions
    return beam_map


def main():
    with open(SCRPIT_DIR / INPUT_DATA, "r") as f:
        data = [[c for c in line] for line in f.read().splitlines()]
    beam_map = find_beam_map(data, (0, -1), RIGHT)
    beam_map = "".join(["".join(line) for line in beam_map])
    print(f"Answer to part 1: {beam_map.count('#')}")

    count = 0
    for direction in DIRECTIONS:
        if direction == UP:
            locations = [(len(data), i) for i in range(len(data[0]))]
        elif direction == DOWN:
            locations = [(-1, i) for i in range(len(data[0]))]
        elif direction == LEFT:
            locations = [(i, len(data[0])) for i in range(len(data))]
        elif direction == RIGHT:
            locations = [(i, -1) for i in range(len(data))]
        for location in locations:
            beam_map = find_beam_map(data, location, direction)
            beam_map = "".join(["".join(line) for line in beam_map])
            count = max(count, beam_map.count('#'))
    print(f"Answer to part 2: {count}")


if __name__ == "__main__":
    main()