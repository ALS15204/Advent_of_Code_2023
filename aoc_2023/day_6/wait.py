import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_DIR / "example.dat"


def find_min_max_start_time(time: int, distance: int) -> int:
    factor = time ** 2 / 4 - distance
    return (
        math.floor(time / 2 - math.sqrt(factor)), 
        math.ceil(time / 2 + math.sqrt(factor))
        )


def get_number_of_wins(time: int, distance: int) -> int:
    adjustment = 0
    start_time, end_time = find_min_max_start_time(time, distance)
    if int(start_time * (time - start_time)) <= distance:
        adjustment -= 1
    return (end_time - start_time) + adjustment


def main():
    with open(INPUT_DATA) as f:
        record_lines = [line.strip("\n") for line in f.readlines()]
    times = [int(t) for t in record_lines[0].split(":")[1].split()]
    distances = [int(d) for d in record_lines[1].split(":")[1].split()]

    product = 1
    for time, distance in zip(times, distances):
        product *= get_number_of_wins(time, distance)
    print(f"Answer to Part 1: {product}")

    product = get_number_of_wins(
        int("".join(list(map(str, times)))), int("".join(list(map(str, distances))))
        )
    print(f"Answer to Part 2: {product}")


if __name__ == "__main__":
    main()