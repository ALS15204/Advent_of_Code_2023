from pathlib import Path
import re
from typing import Dict, List

SCRIPT_PATH = Path(__file__).parent.absolute()

GAME_ID_REGEX = re.compile(r"(?P<game_name>(?<=Game )\d+(?=:))")
GAME_INFO_REGEX = re.compile(
    r"(?P<blue>(\d+(?= blue)))|"
    r"(?P<red>(\d+(?= red)))|"
    r"(?P<green>(\d+(?= green)))"
    )
GAME_CONSTRAINT = {
    "blue": 14,
    "red": 12,
    "green": 13
    }
ALL_COLORS = list(GAME_CONSTRAINT.keys())


def game_string_to_game_info(game_string: str) -> Dict[int, List[Dict[str, int]]]:
    game_info = {}
    game_id = int(GAME_ID_REGEX.search(game_string).group())
    game_info[game_id] = [
        {k: int(v) if v else 0 for k, v in m.groupdict().items()}
        for m in GAME_INFO_REGEX.finditer(game_string)
        ]
    return game_info


def draw_is_possible(one_draw: Dict[str, int]) -> bool:
    return all(
        one_draw[k] <= GAME_CONSTRAINT[k]
        for k in GAME_CONSTRAINT.keys()
    )


def is_game_possible(game_info: Dict[int, List[Dict[str, str]]]) -> bool:
    return all(
        draw_is_possible(one_draw)
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
    with open(SCRIPT_PATH / "input.dat", "r") as f:
        games = [game_string_to_game_info(line.strip("\n")) for line in f.readlines()]
    possible_games = [game for game in games if is_game_possible(game)]
    print(f"Answer to part 1: {sum(list(game.keys())[0] for game in possible_games)}")
    game_powers = [derive_game_power(game) for game in games]
    print(f"Answer to part 2: {sum(game_powers)}")


if __name__ == "__main__":
    main()