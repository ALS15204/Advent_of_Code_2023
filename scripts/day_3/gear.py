from pathlib import Path
from string import punctuation
from typing import Dict, List, Tuple, Set

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_DIR / "input.dat"
VALID_PUNCTUATION = punctuation.replace(".", "")


def get_full_positions_of_string(start_position: Tuple, text: str) -> Tuple[Tuple]:
    """Return a list of all positions of a string in a diagram."""
    line_idx, char_idx = start_position
    return tuple((line_idx, char_idx + i) for i in range(len(text)))


def find_adjacent_coordinates_to_position(position: Tuple) -> List[Tuple]:
    """Return a list of all coordinates adjacent to a position."""
    x, y = position
    return [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1), (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]


def get_position_to_number(one_diagram_line: str, line_number: int) -> Dict[Tuple[Tuple], int]:
    """Return a dictionary that maps the full position of a number in a diagram line to the number itself."""
    position_to_number = {}
    number_string = ""
    for i, char in enumerate(one_diagram_line):
        if char.isdigit():
            number_string += char
        else:
            if number_string:
                position_to_number[
                    get_full_positions_of_string((line_number, i - len(number_string)), number_string)
                    ] = int(number_string)
                number_string = ""
    if number_string:
        position_to_number[
            get_full_positions_of_string(
                (line_number, len(one_diagram_line) - len(number_string)), number_string
                )
            ] = int(number_string)
    return position_to_number


def get_position_to_symbol(one_diagram_line: str, line_number: int) -> Dict[Tuple, str]:
    """Return a dictionary that maps the position of a symbol in a diagram line to the symbol itself."""
    position_to_symbol = {}
    for i, char in enumerate(one_diagram_line):
        if char in VALID_PUNCTUATION:
            position_to_symbol[(line_number, i)] = char
    return position_to_symbol


def find_adjacent_coordiantes_to_number(position: Tuple, number: int) -> Set[Tuple]:
    """Return a list of all coordinates adjacent to a number."""
    number_positions = get_full_positions_of_string(position, str(number))
    adjacent_coordinates = []
    for pos in number_positions:
        adjacent_coordinates.extend(find_adjacent_coordinates_to_position(pos))
    return {pos for pos in adjacent_coordinates if pos not in number_positions}


def main():
    with open(INPUT_DATA, "r") as f:
        diagram_lines = [line.strip("\n") for line in f.readlines()]
    position_to_number = {}
    position_to_symbol = {}
    for i, line in enumerate(diagram_lines):
        position_to_number.update(get_position_to_number(line, i))
        position_to_symbol.update(get_position_to_symbol(line, i))
    
    # PART 1: Find the sum of all numbers that are adjacent to a symbol
    adjacent_numbers = []
    for pos, number in position_to_number.items():
        adjacent_coordinates = find_adjacent_coordiantes_to_number(pos[0], number)
        if any(coord in position_to_symbol for coord in adjacent_coordinates):
            adjacent_numbers.append(number)

    print(f"Answer to part 1: {sum(adjacent_numbers)}")
    
    # PART 2: Find product of the exactly two numbers if they are adjacent to a * symbol
    gear_ratio_sum = 0
    for pos, symbol in position_to_symbol.items():
        if symbol == "*":
            adjacent_coordinates = find_adjacent_coordinates_to_position(pos)
            adjacent_numbers = [
                number for coords, number in position_to_number.items() 
                if any(adj_coord in coords for adj_coord in adjacent_coordinates)
                ]
            if len(adjacent_numbers) == 2:
                gear_ratio_sum += adjacent_numbers[0] * adjacent_numbers[1]
    print(f"Answer to part 2: {gear_ratio_sum}")


if __name__ == "__main__":
    main()
