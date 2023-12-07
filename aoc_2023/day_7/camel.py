from pathlib import Path
from typing import List, Optional, Tuple

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE_PATH = SCRIPT_DIR / "input.dat"
HAND_RANK_SCORE_TO_CARD_COUNT = {
    1: [1, 1, 1, 1, 1],
    2: [2, 1, 1, 1],
    3: [2, 2, 1],
    4: [3, 1, 1],
    5: [3, 2],
    6: [4, 1],
    7: [5]
}
RANKED_CARD_TYPES = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_RANK_SCORE_TO_TYPE = {
    idx: type for idx, type in enumerate(RANKED_CARD_TYPES[::-1], 1)
    }
CARD_TYPE_TO_RANK_SCORE = {v: k for k, v in CARD_RANK_SCORE_TO_TYPE.items()}


def get_rank_score_from_hand(hand_str: str, wild_card: Optional[str] = ""):
    hand = [c for c in hand_str if c != wild_card]
    hand_count = sorted([hand.count(c) for c in set(hand)], reverse=True)
    if wild_card and wild_card in hand_str:
        if hand_count:
            hand_count[0] += hand_str.count(wild_card)
        else:
            hand_count.append(hand_str.count(wild_card))
    return [
        key for key, value in HAND_RANK_SCORE_TO_CARD_COUNT.items() if value == hand_count
        ].pop()


def sort_hand_bid_tuples_of_same_type(
        hand_bid_tuples_list: List[Tuple[str, int]], wild_card: Optional[str] = ""
        ):
    if wild_card:
        ranked_card_types = RANKED_CARD_TYPES.copy()
        ranked_card_types.remove(wild_card)
        ranked_card_types.append(wild_card)
        card_rank_score_to_type = {
            k: v for k, v in enumerate(ranked_card_types[::-1], 1)
            }
        card_type_to_rank_score = {v: k for k, v in card_rank_score_to_type.items()}
    else:
        card_rank_score_to_type = CARD_RANK_SCORE_TO_TYPE
        card_type_to_rank_score = CARD_TYPE_TO_RANK_SCORE

    hands_in_card_type_tuples = [
        (tuple([card_type_to_rank_score[c] for c in hand_str]), bid) 
        for hand_str, bid in hand_bid_tuples_list
        ]
    hands_ranked = sorted(hands_in_card_type_tuples, key=lambda x: x[0])
    return [
        ("".join(card_rank_score_to_type[c] for c in hand), bid) for hand, bid in hands_ranked
        ]

def get_winning_score_from_one_game(hand_bid_tuples, wild_card: Optional[str] = ""):
    hand_bid_tuples_by_type = [[] for _ in range(len(HAND_RANK_SCORE_TO_CARD_COUNT))]
    for hand, bid in hand_bid_tuples:
        hand_rank_score = get_rank_score_from_hand(hand, wild_card=wild_card)
        hand_bid_tuples_by_type[hand_rank_score - 1].append((hand, bid))
    ranked_hand_bid = []
    for hand_bid_tuples_list in hand_bid_tuples_by_type:
        ranked_hand_bid.extend(sort_hand_bid_tuples_of_same_type(hand_bid_tuples_list, wild_card=wild_card))
    winning = 0
    for rank, (hand, bid) in enumerate(ranked_hand_bid, 1):
        winning += rank * int(bid)
    return winning


def main():
    with open(INPUT_FILE_PATH, "r") as f:
        hand_bid_tuples = [tuple(line.strip("\n").split()) for line in f.readlines()]
    winning = get_winning_score_from_one_game(hand_bid_tuples)
    print(f"Answer to Part 1: {winning}")

    winning = get_winning_score_from_one_game(hand_bid_tuples, wild_card="J")
    print(f"Answer to Part 2: {winning}")

if __name__ == '__main__':
    main()
