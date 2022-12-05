from collections import defaultdict
from typing import Dict, List
from util import read_file


Stacks = Dict[int, List[str]]
Instructions = List[str]


class CrateMover:
    @staticmethod
    def rearrange(stacks: Stacks, n_move: int, from_stack: int, to_stack: int) -> Stacks:
        raise NotImplementedError


class CrateMover9000(CrateMover):
    @staticmethod
    def rearrange(stacks: Stacks, n_move: int, from_stack: int, to_stack: int) -> Stacks:
        for _ in range(n_move):
            stacks[to_stack].append(stacks[from_stack].pop())
        return stacks


class CrateMover9001(CrateMover):
    @staticmethod
    def rearrange(stacks: Stacks, n_move: int, from_stack: int, to_stack: int) -> Stacks:
        stacks[to_stack].extend(stacks[from_stack][-n_move:])
        del stacks[from_stack][-n_move:]
        return stacks


def parse_stacks(crates_and_instructions: List[str]) -> Stacks:
    semaphore_idx = crates_and_instructions.index("")

    stack_str = crates_and_instructions[semaphore_idx - 1]
    stack_ids = list(map(int, [el for el in stack_str.split(" ") if el != ""]))
    stack_pos = [stack_str.index(str(s)) for s in stack_ids]

    filled_stack_str = crates_and_instructions[: semaphore_idx - 1]

    # Parse in reverse order to fill the stacks bottom up
    stacks = defaultdict(list)
    for row in filled_stack_str[::-1]:
        for idx, pos in zip(stack_ids, stack_pos):
            if row[pos] != " ":
                stacks[idx].append(row[pos])

    return stacks


def parse_instructions(crates_and_instructions: List[str]) -> Instructions:
    return crates_and_instructions[crates_and_instructions.index("") + 1 :]


def rearrange(stacks: Stacks, instructions: Instructions, crate_mover: CrateMover) -> Stacks:
    for instruction in instructions:
        n_move, from_stack, to_stack = map(int, instruction.split(" ")[1::2])
        stacks = crate_mover.rearrange(stacks, n_move, from_stack, to_stack)
    return stacks


if __name__ == "__main__":
    crates_and_instructions = read_file("input/day5.txt")
    stacks = parse_stacks(crates_and_instructions)
    instructions = parse_instructions(crates_and_instructions)
    stacks = rearrange(stacks, instructions, CrateMover9001())
    print(f"Top crates: {''.join([crates[-1] for crates in stacks.values()])}")
