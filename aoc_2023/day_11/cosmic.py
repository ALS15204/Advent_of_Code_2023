import itertools
from pathlib import Path
from typing import List, Tuple

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / "input.dat"
EMPTY_SPACE = "."
GALAXY = "#"
N_EXP_1 = 2
N_EXP_2 = 1000000
NO_EXPANSION = 0


def expand_map(cosmic_map: List[str], n_exp: int=1) -> List[str]:
    new_cosmic_map = []
    for line in cosmic_map:
        new_cosmic_map.append(line)
        if all(c == EMPTY_SPACE for c in line):
            new_cosmic_map.extend([line]* (n_exp))
    n_new_col = 0
    for col_idx in range(len(cosmic_map[0])):
        if all(line[col_idx] == EMPTY_SPACE for line in cosmic_map):
            for line_idx in range(len(new_cosmic_map)):
                new_cosmic_map[line_idx] = f"{new_cosmic_map[line_idx][:col_idx + n_new_col]}" + \
                f"{EMPTY_SPACE*n_exp}{new_cosmic_map[line_idx][col_idx + n_new_col:]}"
            n_new_col += n_exp
    return new_cosmic_map


def get_galaxy_coordinates_in_map(cosmic_map: List[str]) -> List[tuple]:
    galaxy_coordinates = []
    for line_idx in range(len(cosmic_map)):
        for col_idx in range(len(cosmic_map[0])):
            if cosmic_map[line_idx][col_idx] != EMPTY_SPACE:
                galaxy_coordinates.append((line_idx, col_idx))
    return galaxy_coordinates


def find_shortest_distance_between_coordinates(coord_1: Tuple[int, int], coord_2: Tuple[int, int]) -> int:
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


def find_sum_of_shortest_distances(cosmic_map: List[str], n_exp: int) -> int:
    expanded_cosmic_map = expand_map(cosmic_map, n_exp)
    galaxy_coordinates = get_galaxy_coordinates_in_map(expanded_cosmic_map)
    dist = 0
    for coord_1, coord_2 in itertools.combinations(galaxy_coordinates, 2):
        dist += find_shortest_distance_between_coordinates(coord_1, coord_2)
    return dist


def main():
    with open(INPUT_FILE, "r") as f:
        cosmic_map = [line.strip("\n") for line in f.readlines()]
    dist_n_exp_1 = find_sum_of_shortest_distances(cosmic_map, N_EXP_1 - 1)
    print(f"Answer to Part 1: {dist_n_exp_1}")

    no_expansion_dist = find_sum_of_shortest_distances(cosmic_map, NO_EXPANSION)
    increase_per_expansion = dist_n_exp_1 - no_expansion_dist
    dist_n_exp_2 = dist_n_exp_1 + increase_per_expansion * (N_EXP_2 - N_EXP_1)
    print(f"Answer to Part 2: {dist_n_exp_2}")


if __name__ == "__main__":
    main()