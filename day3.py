import string
from util import read_file


def priority(item: str) -> int:
    return (string.ascii_lowercase + string.ascii_uppercase).index(item) + 1


def get_shared_item(rucksack: str) -> str:
    n_items = len(rucksack) // 2
    first, second = set(rucksack[:n_items]), set(rucksack[n_items:])
    return first.intersection(second).pop()


def score_rucksack(rucksack: str) -> int:
    return priority(get_shared_item(rucksack))


if __name__ == "__main__":

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
