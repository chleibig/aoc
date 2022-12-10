from typing import List, NamedTuple, Set, Tuple

from util import read_file


class Position(NamedTuple):
    row: int
    col: int


def move_along_axis(position: Position, axis: str, step: int) -> Position:
    other_axis = "col" if axis == "row" else "row"
    return Position(**{axis: getattr(position, axis) + step, other_axis: getattr(position, other_axis)})


def delta(head: Position, tail: Position, axis: str) -> int:
    return getattr(head, axis) - getattr(tail, axis)


def move(
    instruction: str, head: Position, tail: Position, visited: Set[Position]
) -> Tuple[Position, Position, Set[Position]]:

    direction, n_steps = instruction.split(" ")
    n_steps = int(n_steps)

    axis = {"L": "col", "R": "col", "U": "row", "D": "row"}[direction]
    other_axis = {"L": "row", "R": "row", "U": "col", "D": "col"}[direction]
    step = {"L": -1, "R": +1, "U": -1, "D": +1}[direction]

    for _ in range(n_steps):
        # Move head
        head = move_along_axis(head, axis, step)
        # Drag tail along if necessary
        if abs(delta(head, tail, axis)) > 1:
            tail = move_along_axis(tail, axis, step)
            # Tail drift
            if delta(head, tail, other_axis) > 0:
                tail = move_along_axis(tail, other_axis, +1)
            elif delta(head, tail, other_axis) < 0:
                tail = move_along_axis(tail, other_axis, -1)
            # One tail step - either along an axis or diagonal - is completed
            visited.add(tail)

    return head, tail, visited


def trace(instructions: List[str]) -> Set[Position]:
    head = Position(row=0, col=0)
    tail = Position(row=0, col=0)
    visited = set(tail)
    for instruction in instructions:
        head, tail, visited = move(instruction, head, tail, visited)
    return visited


if __name__ == "__main__":
    assert len(trace(read_file("input/test_day9.txt"))) == 13
    print(f"Number of tail positions visited at least once: {len(trace(read_file('input/day9.txt')))}")
