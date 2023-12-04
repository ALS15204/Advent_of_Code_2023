from math import log
from pathlib import Path
import re
from typing import Dict, List

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_DIR / "input.dat"

CARD_ID_STRING = "card_id"
CARD_ID_REGEX = re.compile(r"(?:Card[\s]+(?P<" + CARD_ID_STRING + ">\d+): )")
SET_SEPARATOR = "|"
REF_NUMBER = "ref_number"
CARD_NUMBER = "card_number"


def get_card_id_to_game_sets(card_string: str) -> Dict[int, List[str]]:
    card_id_to_sets = dict()
    card_id_match = CARD_ID_REGEX.search(card_string)
    card_id = int(card_id_match.group(CARD_ID_STRING))
    set_list = card_string[card_id_match.end():].split(SET_SEPARATOR)
    card_id_to_sets[card_id] = dict().fromkeys([REF_NUMBER, CARD_NUMBER])
    card_id_to_sets[card_id][REF_NUMBER] = [int(num) for num in set_list[0].split()]
    card_id_to_sets[card_id][CARD_NUMBER] = [int(num) for num in set_list[1].split()]
    return card_id_to_sets


def calculate_card_point(game_set: Dict[str, List[int]]) -> int:
    point = 0
    for card_number in game_set[CARD_NUMBER]:
        if card_number in game_set[REF_NUMBER]:
            point = point + 1 if point == 0 else point * 2
    return point

def main():
    with open(INPUT_DATA, "r") as f:
        card_strings = [line.strip("\n") for line in f.readlines()]
    card_id_to_game_set = {}
    for card_string in card_strings:
        card_id_to_game_set.update(get_card_id_to_game_sets(card_string))

    card_id_to_point = {}
    for card_id, game_set in card_id_to_game_set.items():
        card_id_to_point[card_id] = calculate_card_point(game_set)
    print(f"Answer to part 1: {sum(card_id_to_point.values())}")

    card_id_to_number = dict.fromkeys(card_id_to_point.keys(), 1)
    for card_id in sorted(card_id_to_point.keys()):
        if card_id == len(card_id_to_point):
            break
        number_of_winning_card = int(
            log(card_id_to_point.get(card_id), 2)
            ) + 1 if card_id_to_point.get(card_id) > 0 else 0
        for next_card_id in range(card_id + 1, card_id + number_of_winning_card + 1, 1):
            if next_card_id <= len(card_id_to_point):
                card_id_to_number[next_card_id] += card_id_to_number[card_id]
    print(f"Answer to part 2: {sum(card_id_to_number.values())}")

if __name__ == "__main__":
    main()