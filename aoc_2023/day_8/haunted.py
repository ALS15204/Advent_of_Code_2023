from itertools import cycle
import math
from pathlib import Path
import re
from typing import List, Dict, Tuple

LEFT = 0
RIGHT = 1
ORIGIN = "AAA"
GOAL = "ZZZ"
NODE_REGEX = re.compile(r"(?P<node>[A-Z]+) = \((?P<left>[A-Z]+), (?P<right>[A-Z]+)\)")

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / "input.dat"


def get_rule_sequence(rule_str: str) -> List[int]:
    return [1 if c == "R" else 0 for c in rule_str]


def node_to_left_and_right(node_str: str) -> Dict[str, Tuple[str, str]]:
    m = NODE_REGEX.match(node_str)
    return {m.group("node"): (m.group("left"), m.group("right"))}


def count_steps_to_goal(
        rule: List[int], nodes: Dict[str, Tuple[str, str]], 
        origin: str=ORIGIN, goal: str=GOAL) -> int:
    n_steps = 0
    current_block = origin
    while current_block[-1] != goal[-1]:
        direction = rule[n_steps % len(rule)]
        n_steps += 1
        current_block = nodes[current_block][direction]
    direction = rule[n_steps % len(rule)]
    return n_steps


def main():
    with open(INPUT_FILE, "r") as f:
        lines = [line.strip("\n") for line in f.readlines()]
        lines = [line for line in lines if line]

    rule_sequence = get_rule_sequence(lines[0])
    nodes = {}
    nodes = {k: v for line in lines[1:] for k, v in node_to_left_and_right(line).items()}
    n_steps = count_steps_to_goal(rule_sequence, nodes)
    print(f"Answer to Part 1: {n_steps}")

    n_steps = []
    origin_blocks = [b for b in nodes if b[-1] == "A"]
    for b in origin_blocks:
        n_steps.append(count_steps_to_goal(rule_sequence, nodes, b))
    print(f"Answer to Part 2: {math.lcm(*n_steps)}")

if __name__ == "__main__":
    main()
