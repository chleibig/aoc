from typing import List

from util import read_file


def register(instructions: List[str]) -> List[int]:
    values = []
    x = 1
    for instruction in instructions:
        if instruction == "noop":
            values.append(x)
        elif instruction.startswith("addx"):
            values.extend([x, x])
            x += int(instruction.split(" ")[-1])
        else:
            ValueError(f"Can't parse instruction {instruction}.")
    return values


def signal_strength(values: List[int]) -> int:
    return sum(cycle * values[cycle - 1] for cycle in [20, 60, 100, 140, 180, 220])


def draw_screen(instructions: List[str]) -> str:
    sprite_centers = register(instructions)

    screen = []
    n_rows = 6
    n_cols = 40
    for row in range(n_rows):
        line = ["."] * n_cols
        sc = sprite_centers[row * n_cols : (row + 1) * n_cols]
        for col in range(n_cols):
            if abs(col - sc[col]) <= 1:
                line[col] = "#"
        screen.extend(line)
        screen.append("\n")

    return "".join(screen)


if __name__ == "__main__":
    assert signal_strength(register(read_file("input/test_day10.txt"))) == 13140
    print(f"Part one: {signal_strength(register(read_file('input/day10.txt')))}")
    print("\nPart two:\n")
    print(draw_screen(read_file("input/day10.txt")))
