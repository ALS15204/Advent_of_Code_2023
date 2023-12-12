from functools import cache
import itertools
from pathlib import Path
from typing import List

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "input.dat"
BROKEN = "#"
UNKNOWN = "?"
N_EXPANSION = 5
CACHE = {}


def count_broken_spring_groups(spring_line: str) -> List[int]:
    broken_spring_groups = []
    current_group = 0
    for spring in spring_line:
        if spring == BROKEN:
            current_group += 1
        elif current_group > 0:
            broken_spring_groups.append(current_group)
            current_group = 0
    if current_group > 0:
        broken_spring_groups.append(current_group)
    return broken_spring_groups



def find_possible_combinations(spring_line, groups, i, bi, current):
  key = (i, bi, current)
  if key in CACHE:
    return CACHE[key]
  if i==len(spring_line):
    if bi==len(groups) and current==0:
      return 1
    elif bi==len(groups)-1 and groups[bi]==current:
      return 1
    else:
      return 0
  ans = 0
  for c in ['.', '#']:
    if spring_line[i]==c or spring_line[i]=='?':
      if c=='.' and current==0:
        ans += find_possible_combinations(spring_line, groups, i+1, bi, 0)
      elif c=='.' and current>0 and bi<len(groups) and groups[bi]==current:
        ans += find_possible_combinations(spring_line, groups, i+1, bi+1, 0)
      elif c=='#':
        ans += find_possible_combinations(spring_line, groups, i+1, bi, current+1)
  CACHE[key] = ans
  return ans


def main():
    with open(INPUT_FILE) as f:
        spring_group_lines = [tuple(line.strip("\n").split()) for line in f.readlines()]
    spring_line_groups = [
        (spring_line, list(map(int, group.split(",")))) for spring_line, group in spring_group_lines
        ]
    n_combinations = 0
    for spring_line, groups in spring_line_groups:
        CACHE.clear()
        if groups == count_broken_spring_groups(spring_line):
            n_combinations += 1
        else:
            n_combinations += find_possible_combinations(spring_line, groups, 0, 0, 0)
    print(f"Answer to Part 1: {n_combinations}")

    n_combinations = 0
    for spring_line, groups in spring_line_groups:
        CACHE.clear()
        new_spring_line = "?".join([spring_line] * N_EXPANSION)
        new_groups = groups * N_EXPANSION
        if groups == count_broken_spring_groups(new_spring_line):
            n_combinations += 1
        else:
            n_combinations += find_possible_combinations(new_spring_line, new_groups, 0, 0, 0)
    print(f"Answer to Part 2: {n_combinations}")


if __name__ == "__main__":
    main()