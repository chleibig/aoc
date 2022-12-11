from collections import defaultdict
from dataclasses import dataclass
import math
from typing import Callable, Dict, List
from util import read_file


@dataclass
class Monkey:
    items: List[int]
    get_worry_level: Callable[[int], int]
    throw_to: Callable[[int], int]


def expression2code(expression: str):
    arg1, operator, arg2 = expression.split(" ")
    if arg2 != "old":
        if operator == "*":

            def code(old: int) -> int:
                return old * int(arg2)

        elif operator == "+":

            def code(old: int) -> int:
                return old + int(arg2)

    else:
        if operator == "*":

            def code(old: int) -> int:
                return old * old

        elif operator == "+":

            def code(old: int) -> int:
                return old + old

    return code


def create_monkey(notes: List[str], reduce_worry_level: int) -> Monkey:
    assert len(notes) == 5
    items = list(map(int, notes[0].removeprefix("Starting items: ").split(",")))

    expression = notes[1].removeprefix("Operation: new = ")
    code = expression2code(expression)
    if reduce_worry_level == 3:
        get_worry_level = lambda old: code(old) // reduce_worry_level
    else:
        get_worry_level = lambda old: code(old % reduce_worry_level)

    divide_by = int(notes[2].removeprefix("Test: divisible by "))
    true_monkey = int(notes[3].removeprefix("  If true: throw to monkey "))
    false_monkey = int(notes[4].removeprefix("  If false: throw to monkey "))
    throw_to = lambda w: true_monkey if (w % divide_by) == 0 else false_monkey

    return Monkey(items, get_worry_level, throw_to)


def split_by_monkey(notes: List[str]) -> Dict[int, List[str]]:
    notes_by_monkey = defaultdict(list)
    current_monkey = None
    for line in notes:
        if line.startswith("Monkey"):
            current_monkey = int(line.removeprefix("Monkey ").strip(":"))
            continue
        if line == "":
            continue
        notes_by_monkey[current_monkey].append(line[2:])  # remove whitespace
    return notes_by_monkey


def get_divisor_product(notes_by_monkeys: Dict[int, List[str]]) -> int:
    divide_by = 1
    for notes in notes_by_monkeys.values():
        divide_by *= int(notes[2].removeprefix("Test: divisible by "))
    return divide_by


def play(filename: str, n_rounds: int, reduce_worry_level: str) -> int:
    notes = read_file(filename)
    notes_by_monkeys = split_by_monkey(notes)

    # Patch get_worry_level with reduction method
    if reduce_worry_level == "part_1":
        reduce_worry_level = 3
    elif reduce_worry_level == "part_2":
        # Chinese remainder theorem?
        reduce_worry_level = get_divisor_product(notes_by_monkeys)
    else:
        ValueError(f"Can't parse reduce_worry_level={reduce_worry_level}.")

    monkeys = {monkey: create_monkey(notes, reduce_worry_level) for monkey, notes in notes_by_monkeys.items()}

    items_inspected = defaultdict(int)
    for _ in range(n_rounds):
        for key, monkey in monkeys.items():
            items_inspected[key] += len(monkey.items)

            def throw(item: int):
                item = monkey.get_worry_level(item)
                return item, monkey.throw_to(item)

            for item, target in map(throw, monkey.items):
                monkeys[target].items.append(item)
            monkey.items.clear()

    return math.prod(sorted(items_inspected.values())[::-1][:2])


if __name__ == "__main__":
    assert play("input/test_day11.txt", n_rounds=20, reduce_worry_level="part_1") == 10605
    print(f"Part one: {play('input/day11.txt', n_rounds=20, reduce_worry_level='part_1')}")
    assert play("input/test_day11.txt", n_rounds=10000, reduce_worry_level="part_2") == 2713310158
    print(f"Part two: {play('input/day11.txt', n_rounds=10000, reduce_worry_level='part_2')}")
