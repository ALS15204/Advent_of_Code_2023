from pathlib import Path
from typing import List

SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / 'input.dat'
N_SMUDGE = 1


def find_reflection_row(pattern: List[str], n_smudge: int = 0) -> int:
    for i, _ in enumerate(pattern):
        if i == len(pattern) - 1:
            return 0
        smudge_credit = n_smudge
        for p_back, p_forward in zip(pattern[:i + 1][::-1], pattern[i + 1:]):
            match = True
            if p_back == p_forward:
                continue
            elif smudge_credit > 0 and sum(
                [c_back != c_forward for c_back, c_forward in zip(p_back, p_forward)]
                ) == 1:
                smudge_credit -= 1
                continue
            else:
                match = False
                break
        if match and smudge_credit == 0:
            return i + 1
    return 0
            

def find_reflection_col(pattern: List[str], n_smudge: int = 0) -> int:
    pattern_by_column = [''.join(col) for col in zip(*pattern)]
    return find_reflection_row(pattern_by_column, n_smudge=n_smudge)


def main():
    with open(INPUT_DATA, 'r') as f:
        patterns = f.read().split("\n\n")
        patterns = [pattern.split("\n") for pattern in patterns]
        patterns = [[p for p in pattern if p] for pattern in patterns]

    score = 0
    for pattern in patterns:
        col, row = find_reflection_col(pattern), find_reflection_row(pattern)
        score += col + 100 * row
    print(f"Answr to Part 1: {score}")

    score = 0
    for pattern in patterns:
        col, row = find_reflection_col(pattern, N_SMUDGE), find_reflection_row(pattern, N_SMUDGE)
        score += col + 100 * row
    print(f"Answr to Part 2: {score}")


if __name__ == '__main__':
    main()