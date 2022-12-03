from typing import List


def read_file(filename: str) -> List[str]:
    with open(filename) as h:
        return h.read().splitlines()
