from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_DATA = SCRIPT_DIR / "input.dat"


def find_min_start_time(time: int, distance: int) -> int:
    start_time = distance // time
    for t in range(start_time, 0, -1):
        if t * (time - t) < distance:
            return t + 1
    return 1

def get_number_of_wins(time: int, distance: int) -> int:
    count = 0
    start_time = find_min_start_time(time, distance)
    for t in range(start_time, time + 1):
        if t * (time - t) > distance:
            count += 1
        elif count > 0:
            break
    return count


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