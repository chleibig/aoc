from typing import List

from util import read_file


def run(instructions: List[str]) -> List[int]:
    values = []
    next = 1
    for instruction in instructions:
        if instruction == "noop":
            values.append(next)
        elif instruction.startswith("addx"):
            values.extend([next, next])
            next += int(instruction.split(" ")[-1])
        else:
            ValueError(f"Can't parse instruction {instruction}.")
    return values


def signal_strength(values: List[int]) -> int:
    return sum(cycle * values[cycle - 1] for cycle in [20, 60, 100, 140, 180, 220])


if __name__ == "__main__":
    assert signal_strength(run(read_file("input/test_day10.txt"))) == 13140
    print(f"Part one: {signal_strength(run(read_file('input/day10.txt')))}")
