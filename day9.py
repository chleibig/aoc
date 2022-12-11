from typing import List, NamedTuple, Set, Tuple

from util import read_file


def sign(x: int) -> int:
    if x > 0:
        return +1
    elif x == 0:
        return 0
    else:
        return -1


class Position(NamedTuple):
    row: int
    col: int


def move_along_axis(position: Position, axis: str, step: int) -> Position:
    other_axis = "col" if axis == "row" else "row"
    return Position(**{axis: getattr(position, axis) + step, other_axis: getattr(position, other_axis)})


def is_touching(head: Position, tail: Position) -> bool:
    return (abs(head.row - tail.row) <= 1) and (abs(head.col - tail.col) <= 1)


def drag_along(head: Position, tail: Position) -> Position:
    # Deltas along the two axes will either be {|2|, |1|} or {|2|, |0|}
    delta_row = head.row - tail.row
    delta_col = head.col - tail.col
    # What we want: {|2|, |1|} => {|1|, |0|} or {|2|, |0|} => {|1|, |0|}
    # Hence we always move by -1, 0 or +1
    return move_along_axis(move_along_axis(tail, "row", sign(delta_row)), "col", sign(delta_col))


def move(instruction: str, rope: List[Position], visited: Set[Position]) -> Tuple[List[Position], Set[Position]]:

    direction, n_steps = instruction.split(" ")
    n_steps = int(n_steps)

    axis = {"L": "col", "R": "col", "U": "row", "D": "row"}[direction]
    step = {"L": -1, "R": +1, "U": -1, "D": +1}[direction]

    n_knots = len(rope)
    for _ in range(n_steps):
        # Move head
        rope[0] = move_along_axis(rope[0], axis, step)
        # Move rest
        for i in range(n_knots - 1):
            knot, next_knot = rope[i], rope[i + 1]
            if not is_touching(knot, next_knot):
                rope[i + 1] = drag_along(knot, next_knot)
        # Track tail position
        visited.add(rope[-1])

    return rope, visited


def trace(instructions: List[str], n_knots: int) -> Set[Position]:
    rope = [Position(row=0, col=0) for _ in range(n_knots)]
    visited = {rope[-1]}
    for instruction in instructions:
        rope, visited = move(instruction, rope, visited)
    return visited


if __name__ == "__main__":
    assert len(trace(read_file("input/test_day9.txt"), 2)) == 13
    assert len(trace(read_file("input/test_day9.txt"), 10)) == 1
    assert len(trace(read_file("input/test_day9_2.txt"), 10)) == 36

    print(f"Part one: {len(trace(read_file('input/day9.txt'), 2))}")
    print(f"Part two: {len(trace(read_file('input/day9.txt'), 10))}")
