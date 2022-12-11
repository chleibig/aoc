from collections import defaultdict
from dataclasses import dataclass
import math
from typing import Callable, Dict, List, Optional
from util import read_file


@dataclass
class Monkey:
    items: List[int]
    get_worry_level: Callable[[int], int]
    throw_to: Callable[[int], int]


def create_monkey(notes: List[str]) -> Monkey:
    assert len(notes) == 5
    items = list(map(int, notes[0].removeprefix("Starting items: ").split(",")))

    expression = notes[1].removeprefix("Operation: new = ")
    get_worry_level = lambda old: int(math.floor(eval(expression) / 3))

    divide_by = int(notes[2].removeprefix("Test: divisible by "))
    true_monkey = int(notes[3].removeprefix("  If true: throw to monkey "))
    false_monkey = int(notes[4].removeprefix("  If false: throw to monkey "))
    throw_to = lambda w: true_monkey if (w % divide_by) == 0 else false_monkey

    return Monkey(items, get_worry_level, throw_to)


def split_by_monkey(notes: List[str]) -> Dict[str, List[str]]:
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


def play(filename: str, n_rounds: int) -> int:
    notes = read_file(filename)
    notes_by_monkeys = split_by_monkey(notes)
    monkeys = {monkey: create_monkey(notes) for monkey, notes in notes_by_monkeys.items()}

    items_inspected = defaultdict(int)
    for _ in range(n_rounds):
        for key, monkey in monkeys.items():
            items_inspected[key] += len(monkey.items)
            while len(monkey.items) > 0:
                item = monkey.get_worry_level(monkey.items[0])
                monkeys[monkey.throw_to(item)].items.append(item)
                del monkey.items[0]
    return math.prod(sorted(items_inspected.values())[::-1][:2])


if __name__ == "__main__":
    assert play("input/test_day11.txt", n_rounds=20) == 10605
    print(f"Part one: {play('input/day11.txt', n_rounds=20)}")
