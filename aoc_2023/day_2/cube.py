from pathlib import Path
import re
from typing import Dict, List

SCRIPT_PATH = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_PATH / "input.dat"
GAME_ID_STRING = "game_id"
BLUE = "blue"
RED = "red"
GREEN = "green"

GAME_ID_REGEX = re.compile(r"(?:Game (?P<" + GAME_ID_STRING + ">\d+): )")
GAME_INFO_REGEX = re.compile(
    r"(?P<blue>(\d+(?= " + BLUE + ")))|"
    r"(?P<red>(\d+(?= " + RED + ")))|"
    r"(?P<green>(\d+(?= " + GREEN + ")))"
    )
GAME_CONSTRAINT = {
    BLUE: 14,
    RED: 12,
    GREEN: 13
    }
ALL_COLORS = list(GAME_CONSTRAINT.keys())


def get_color_to_number_per_draw(draw_string: str) -> Dict[str, int]:
    color_to_number_per_draw = dict.fromkeys(ALL_COLORS, 0)
    for color in ALL_COLORS:
        for m in GAME_INFO_REGEX.finditer(draw_string):
            if m.group(color):
                color_to_number_per_draw[color] = int(m.group(color))
    return color_to_number_per_draw


def get_game_id_to_draws(game_string: str) -> Dict[int, List[Dict[str, int]]]:
    game_id_to_draws = {}
    game_id_match = GAME_ID_REGEX.search(game_string)
    game_id = int(game_id_match.group(GAME_ID_STRING))
    draw_info_list = []
    for draw_string in game_string[game_id_match.end():].split(";"):
        draw_info_list.append(get_color_to_number_per_draw(draw_string))
    game_id_to_draws[game_id] = draw_info_list
    return game_id_to_draws


def is_draw_possible(one_draw: Dict[str, int]) -> bool:
    return all(
        one_draw[k] <= GAME_CONSTRAINT[k]
        for k in GAME_CONSTRAINT.keys()
    )


def is_game_possible(game_info: Dict[int, List[Dict[str, str]]]) -> bool:
    return all(
        is_draw_possible(one_draw)
        for one_draw in list(game_info.values())[0]
        )

def derive_game_power(game_info: Dict[int, List[Dict[str, str]]]) -> int:
    color_to_number = dict.fromkeys(ALL_COLORS, 0)
    for one_draw in list(game_info.values())[0]:
        for color in ALL_COLORS:
            if one_draw[color] > color_to_number[color]:
                color_to_number[color] = one_draw[color]
    power = 1
    for color in ALL_COLORS:
        power *= color_to_number[color]
    return power


def main():
    with open(INPUT_DATA, "r") as f:
        games = [get_game_id_to_draws(line.strip("\n")) for line in f.readlines()]
    possible_games = [game for game in games if is_game_possible(game)]
    print(f"Answer to part 1: {sum(list(game.keys())[0] for game in possible_games)}")
    game_powers = [derive_game_power(game) for game in games]
    print(f"Answer to part 2: {sum(game_powers)}")


if __name__ == "__main__":
    main()