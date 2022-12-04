from typing import Set, Tuple
from util import read_file


def parse_range(idrange: str) -> Set:
    start, stop = map(int, idrange.split("-"))
    return set(range(start, stop + 1))


def parse_pair(pair: str) -> Tuple:
    return tuple(map(parse_range, pair.split(",")))


def is_fully_contained(set1: Set[int], set2: Set[int]) -> bool:
    """Order invariant subset"""
    return set1.issubset(set2) or set2.issubset(set1)


if __name__ == "__main__":
    section_id_pairs = read_file("input/day4.txt")
    n_fully_contained = sum([is_fully_contained(*parse_pair(pair)) for pair in section_id_pairs])
    print(f"There is {n_fully_contained} pairs for which one range is fully contained by the other.")
