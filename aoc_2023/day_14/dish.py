import itertools
from pathlib import Path
from typing import List

SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "input.dat"

ROUND = "O"
SQAURE = "#"
EMPTY = "."

NORTH = "N"
EAST = "E"
WEST = "W"
SOUTH = "S"

N_CYCLE = 1000000000
CACHE = {}


def find_longest_repetition(seq: List[int]) -> int:
    seq = list(map(str, seq))
    repetition = ""
    rep_seq = []
    for element in seq:
        if "".join(seq).count(repetition + element) > 1:
            repetition += element
            rep_seq.append(int(element))
    return rep_seq


def tilt_map(map_data: List[str], direction: str=NORTH) -> List[str]:
    if direction in {NORTH, SOUTH}:
        map_data = ["".join(cs) for cs in zip(*map_data)]
    if direction in {EAST, SOUTH}:
        map_data = [l[::-1] for l in map_data]
    hash_map = hash("".join(map_data))
    new_map_data = []
    for map_line in map_data:
        n_move = 0
        map_line_list = [c for c in map_line]
        for idx, c in enumerate(map_line):
            if c is EMPTY:
                n_move += 1
            elif c is ROUND and n_move > 0:
                map_line_list[idx - n_move] = ROUND
                map_line_list[idx] = EMPTY
            else:
                n_move = 0
        new_map_data.append("".join(map_line_list))
    if direction in {EAST, SOUTH}:
        new_map_data = [l[::-1] for l in new_map_data]
    if direction in {NORTH, SOUTH}:
        new_map_data = ["".join(cs) for cs in zip(*new_map_data)]
    return new_map_data
 

def count_load(map_data: List[str]) -> int:
    load = 0
    for idx, map_line in enumerate(map_data[::-1], 1):
        n_round = map_line.count(ROUND)
        load += n_round * idx
    return load

               
def main():
    with open(INPUT_DATA, "r") as fp:
        data = [l.strip("\n") for l in fp.readlines()]
        data = [l for l in data if l]
    tilted_map = tilt_map(data)
    load = count_load(tilted_map)
    print(f"Answer to part 1: {load}")

    tilted_map = data
    for i in range(N_CYCLE):
        map_in_cycle = tilted_map
        map_key = "\n".join("".join(row) for row in map_in_cycle)
        if map_key in CACHE:
            cycle = i - CACHE[map_key]
            i += (N_CYCLE - i) // cycle * cycle
            if i == N_CYCLE:
                break
        CACHE[map_key] = i
        for d in [NORTH, WEST, SOUTH, EAST]:
            map_in_cycle = tilt_map(map_in_cycle, d)
        tilted_map = map_in_cycle
    load = count_load(tilted_map)
    print(f"Answer to part 2: {load}")


if __name__ == "__main__":
    main()