import math
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / "input.dat"

STARTING_SHAPE = "S"
VOID_SHAPE = "."
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
SHAPE_TO_CONNECTION = {
    "|": {UP, DOWN},
    "-": {LEFT, RIGHT},
    "L": {UP, RIGHT},
    "J": {UP, LEFT},
    "7": {DOWN, LEFT},
    "F": {DOWN, RIGHT}
}
HORIZONTAL_POINT = {
    "|": (0, 0),
    "-": (1, 1),
    "L": (0, 1),
    "J": (1, 0),
    "7": (1, 0),
    "F": (0, 1)
 }
VERTICAL_POINT = {
    "|": (1, 1),
    "-": (0, 0),
    "L": (1, 0),
    "J": (1, 0),
    "7": (0, 1),
    "F": (0, 1)
 }


def is_connected(tile_1: Tuple[Tuple[int, int], str], tile_2: Tuple[Tuple[int, int], str]) -> bool:
    tile_1_coord, tile_1_shape = tile_1
    tile_2_coord, tile_2_shape = tile_2
    tile_2_to_tile_1 = (tile_2_coord[0] - tile_1_coord[0], tile_2_coord[1] - tile_1_coord[1])
    tile_1_to_tile_2 = (-tile_2_to_tile_1[0], -tile_2_to_tile_1[1])
    if tile_1_shape == VOID_SHAPE or tile_2_shape == VOID_SHAPE:
        return False
    if tile_1_shape == STARTING_SHAPE:
        return tile_1_to_tile_2 in SHAPE_TO_CONNECTION[tile_2_shape]
    if tile_2_shape == STARTING_SHAPE:
        return tile_2_to_tile_1 in SHAPE_TO_CONNECTION[tile_1_shape]
    return (
        tile_2_to_tile_1 in SHAPE_TO_CONNECTION[tile_1_shape] 
        and tile_1_to_tile_2 in SHAPE_TO_CONNECTION[tile_2_shape]
        )


def sum_tuple_list_by_element(tuple_list: List[Tuple[int, int]]) -> Tuple[int, int]:
    sum_0, sum_1 = 0, 0
    for element in tuple_list:
        sum_0 += element[0]
        sum_1 += element[1]
    return (sum_0, sum_1)


def main():
    with open(INPUT_FILE, "r") as fp:
        maze = {}
        for row, line in enumerate(fp):
            for col, char in enumerate(line.strip()):
                maze[(row, col)] = char
    starting_point = [(coord, shape) for coord, shape in maze.items() if shape == STARTING_SHAPE].pop()
    first_points = [
        (coord, shape) for coord, shape in maze.items() 
        if coord != starting_point[0] and is_connected((coord, shape), starting_point)
        ]
    first_points_to_starting_point = {
        (coord[0] - starting_point[0][0], coord[1] - starting_point[0][1]) for coord, _ in first_points
        }
    starting_point_shape = [
        shape for shape, connections in SHAPE_TO_CONNECTION.items() if first_points_to_starting_point == connections
        ].pop()
    first_point = first_points.pop()
    connection = {key: -1 for key in maze.keys()}
    path = [starting_point, first_point]
    n_step = 1
    connection[starting_point[0]] = 0
    connection[first_point[0]] = n_step
    current_point = first_point
    while current_point:
        current_point = [
            (coord, shape) for coord, shape in maze.items() 
            if coord != current_point[0] and is_connected((coord, shape), current_point) and (coord, shape) not in path
            ]
        if current_point:
            current_point = current_point.pop()
            path.append(current_point)
            n_step += 1
            connection[current_point[0]] = n_step

    farthest_distance = math.ceil(max([value for value in connection.values() if value]) / 2)
    print(f"Answer to Part 1: {farthest_distance}")

    maze[starting_point[0]] = starting_point_shape
    n_col = max([coord[1] for coord in maze.keys()]) + 1
    n_row = max([coord[0] for coord in maze.keys()]) + 1
    n_tile = 0
    for row in range(n_row):
        for col in range(n_col):
            if ((row, col), maze[(row, col)]) in path:
                continue
            else:
                path_in_same_row = [path_point for path_point in path if path_point[0][0] == row]
                path_in_same_col = [path_point for path_point in path if path_point[0][1] == col]
                horizontal_up = min(sum_tuple_list_by_element([
                    HORIZONTAL_POINT[path_point[1]] for path_point in path_in_same_col if path_point[0][0] < row
                    ]))
                horizontal_down = min(sum_tuple_list_by_element([
                    HORIZONTAL_POINT[path_point[1]] for path_point in path_in_same_col if path_point[0][0] > row
                    ]))
                vertical_left = min(sum_tuple_list_by_element([
                    VERTICAL_POINT[path_point[1]] for path_point in path_in_same_row if path_point[0][1] < col
                    ]))
                vertical_right = min(sum_tuple_list_by_element([
                    VERTICAL_POINT[path_point[1]] for path_point in path_in_same_row if path_point[0][1] > col
                    ]))
                if all(point % 2 == 1 for point in [horizontal_up, horizontal_down, vertical_left, vertical_right]):
                    n_tile += 1
    print(f"Answer to Part 2: {n_tile}")

if __name__ == "__main__":
    main()