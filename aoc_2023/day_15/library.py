from collections import OrderedDict
from pathlib import Path
import re

SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "input.dat"
LABEL = "label"
OPERATION = "operation"
VALUE = "value"
HASHMAP_REGEX = re.compile(
    r"(?P<" + LABEL + ">[a-z]+)"
    r"(?P<" + OPERATION + ">[=-])"
    r"(?P<" + VALUE + ">\d)?"
    )


def hash_string(string: str) -> int:
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def main():
    with open(INPUT_DATA) as f:
        hash_data = f.read().strip().replace("\n", "").split(",")
    code = 0
    for hash_str in hash_data:
        code += hash_string(hash_str)
    print(f"Answer to Part 1: {code}")

    box_to_lens = {}
    for hash_str in hash_data:
        m = HASHMAP_REGEX.match(hash_str)
        box_num = hash_string(m[LABEL])
        if box_num not in box_to_lens:
            box_to_lens[box_num] = OrderedDict()
        if m[OPERATION] == "=":
            box_to_lens[box_num][m[LABEL]] = int(m[VALUE])
        if m[OPERATION] == "-" and m[LABEL] in box_to_lens[box_num]:
            box_to_lens[box_num].pop(m[LABEL])
    f_power_sum = 0
    for box_num, lens_to_focal_length in box_to_lens.items():
        f_power = 1 + box_num
        for idx, (_, focal_length) in enumerate(lens_to_focal_length.items(), 1):
            f_power_sum += f_power * idx * focal_length
    print(f"Answer to Part 2: {f_power_sum}")

if __name__ == "__main__":
    main()
