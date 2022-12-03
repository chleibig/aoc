import string
from typing import List
from util import read_file


def priority(item: str) -> int:
    return (string.ascii_lowercase + string.ascii_uppercase).index(item) + 1


def get_shared_item(rucksack: str) -> str:
    n_items = len(rucksack) // 2
    first, second = set(rucksack[:n_items]), set(rucksack[n_items:])
    return first.intersection(second).pop()


def score_rucksack(rucksack: str) -> int:
    return priority(get_shared_item(rucksack))


def get_rucksack_groups(rucksacks: List[str]) -> List[List[str]]:
    return [rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3)]


def get_badge_item(rucksack_group: List[str]) -> str:
    assert len(rucksack_group) == 3
    return set.intersection(*[set(r) for r in rucksack_group]).pop()


def score_rucksack_group(rucksack_group: List[str]) -> int:
    return priority(get_badge_item(rucksack_group))


if __name__ == "__main__":

    print("Part one")
    test_rucksacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    test_scores = [16, 38, 42, 22, 20, 19]
    for r, s in zip(test_rucksacks, test_scores):
        assert score_rucksack(r) == s, f"{r}, {s}"

    rucksacks = read_file("input_day3.txt")
    print(f"Total priority is {sum(score_rucksack(r) for r in rucksacks)}")

    print("Part two")
    test_rucksacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert sum(score_rucksack_group(rg) for rg in get_rucksack_groups(test_rucksacks)) == 70

    print(f"Total priority is {sum(score_rucksack_group(rg) for rg in get_rucksack_groups(rucksacks))}")
