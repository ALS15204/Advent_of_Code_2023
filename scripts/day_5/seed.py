from pathlib import Path
import re
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_DIR / "input.dat"
SOURCE = "source"
DESTINATION = "destination"
MAPPING = "mapping"
SEED = "seed"
LOCATION = "location"
SOURCE_TO_DESTINATION_REGEX = re.compile(r"(?P<" + SOURCE + ">[a-z]+)-to-(?P<" + DESTINATION + ">[a-z]+) map:")


def get_seed_numbers(seed_string: str) -> List[int]:
    return [int(num.strip()) for num in seed_string.strip("seed:").split()]


def create_mapping(mapping_lines: List[str]) -> Dict[Tuple[int, int], Dict[Tuple[int, int], Tuple[int, int]]]:
    source_to_destination_match = SOURCE_TO_DESTINATION_REGEX.match(mapping_lines[0])
    source_to_destination = dict()
    source, destination = source_to_destination_match.group(SOURCE), source_to_destination_match.group(DESTINATION)
    source_to_destination[(source, destination)] = {}
    for line in mapping_lines[1:]:
        if not line:
            continue
        destinatin_start,  source_start, length = [num for num in map(int, line.split())]
        source_to_destination[(source, destination)][(source_start, source_start + length - 1)] = (
            destinatin_start, destinatin_start + length - 1
            )
    return source_to_destination


def find_mapped_code(
        source_to_destination: Dict[Tuple[int, int], Tuple[int, int]], code: int
        ) -> int:
    source_in_interval = [
        destination[0] + code - source[0] for source, destination in source_to_destination.items() 
        if source[0] <= code <= source[1]
        ]
    return source_in_interval.pop() if source_in_interval else code


def main():
    with open(INPUT_DATA, "r") as f:
        data_string = "".join(f.readlines())
    mapping_line_chunks = data_string.split("\n\n")
    mappings = {}
    seeds = get_seed_numbers(mapping_line_chunks[0])
    source_to_location_sequence = [SEED]
    for mapping_line_chunk in mapping_line_chunks[1:]:
        mapping_dict = create_mapping(mapping_line_chunk.split("\n"))
        mappings.update(mapping_dict)
        source_to_location_sequence.append([key[1] for key in mapping_dict.keys()][0])

    seed_to_location = dict.fromkeys(seeds, None)
    for seed in seeds:
        code = seed
        for source, destination in zip(
            source_to_location_sequence[:-1], source_to_location_sequence[1:]
            ):
            code = find_mapped_code(mappings[(source, destination)], code)
        seed_to_location[seed] = code
    print(f"Answer to Part 1: {min(seed_to_location.values())}")

    min_location = None
    min_set_idx = None
    min_seed = None
    interval = 2
    n_range= int(len(seeds) / interval)
    for set_idx in range(n_range):
        start_idx = set_idx * interval
        seed_start, length = seeds[start_idx: start_idx + interval]
        seed = seed_start
        while seed < seed_start + length:
            code = seed
            for source, destination in zip(
                source_to_location_sequence[:-1], source_to_location_sequence[1:]
                ):
                code = find_mapped_code(mappings[(source, destination)], code)
            if min_location is None or code < min_location:
                print(set_idx, seed)
                min_set_idx = set_idx
                min_seed = seed
                min_location = code
            seed += 10000

    set_idx = min_set_idx
    start_idx = set_idx * interval
    seed_start, length = seeds[start_idx: start_idx + interval]
    seed = min_seed
    while seed_start <= seed < seed_start + length:
        code = seed
        for source, destination in zip(
            source_to_location_sequence[:-1], source_to_location_sequence[1:]
            ):
            code = find_mapped_code(mappings[(source, destination)], code)
        if code < min_location:
            print(set_idx, seed)
            min_location = code
        elif code > min_location:
            break
        seed -= 1


    print(f"Answer to Part 2: {min_location}")


if __name__ == "__main__":
    main()