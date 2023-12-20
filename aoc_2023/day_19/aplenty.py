import os
from pathlib import Path
import re
from typing import List


SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "input.dat"
X = "x"
M = "m"
A = "a"
S = "s"
PARTS_REGEX = re.compile(r"{x=(?P<" + X + ">\d+),m=(?P<" + M + ">\d+),a=(?P<" + A + ">\d+),s=(?P<" + S + ">\d+)}")
RELATION_REGEX = re.compile(r"(?P<var>[xmas])(?P<op>[><=])(?P<val>\d+)")
ACCEPT = "A"
REJECT = "R"
FINAL_RESULTS = {ACCEPT, REJECT}

INITIAL = "in"
GREATERTHAN = ">"
LESSTHAN = "<"
EQUALS = "="
COMPARISON_OPERATORS = {GREATERTHAN, LESSTHAN, EQUALS}
OP_TO_OPPOSITE = {
    OP: {COM for COM in COMPARISON_OPERATORS if COM != OP} for OP in COMPARISON_OPERATORS
    }


def parse_rule(rule: str):
    rule_name, rule_parts_str = rule.split("{")
    rule_parts = rule_parts_str.strip("}").split(",")
    return (rule_name, rule_parts)


def parse_part(part: str):
    part_match = re.match(PARTS_REGEX, part)
    return {k : int(v) for k, v in part_match.groupdict().items()}


def sort_part_by_rules(part: str, rules: list) -> str:
    for name, value in part.items():
        exec(f"{name}={value}")
    for rule in rules:
        if any(compare in rule for compare in COMPARISON_OPERATORS):
            relation, result = rule.split(":")
            if eval(relation):
                return result
        else:
            return rule

            
def sort_part(part: str, name_to_rules: dict) -> str:
    rule_name = INITIAL
    while rule_name not in FINAL_RESULTS:
        rules = name_to_rules[rule_name]
        rule_name = sort_part_by_rules(part, rules)
    return rule_name
            

def main():
    with open(INPUT_DATA) as f:
        data = f.read().splitlines()
    rules = data[:data.index("")]
    name_to_rules = {}
    for rule in rules:
        rule_name, rule_parts = parse_rule(rule)
        name_to_rules[rule_name] = rule_parts
    parts = data[data.index("") + 1:]
    parts = [parse_part(part) for part in parts]
    sum_parts = 0
    for part in parts:
        if sort_part(part, name_to_rules) == ACCEPT:
            sum_parts += sum(part.values())
    print(f"Answer to Part 1: {sum_parts}")

    count = 0
    for x in range(4001):
        for m in range(4001):
            for a in range(4001):
                for s in range(4001):
                    part = {X: x, M: m, A: a, S: s}
                    if sort_part(part, name_to_rules) == ACCEPT:
                        count += 1
                        print(count)
    print(f"Answer to Part 2: {count}")


if __name__ == "__main__":
    main()