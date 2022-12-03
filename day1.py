from typing import List


def read_file() -> List[str]:
    with open("input_day1.txt") as h:
        return h.read().splitlines()


def calories_per_elf(calories: List[str]) -> List[int]:
    total_calories_per_elf = []
    calories_one_elf = []
    for cal in calories:
        if cal != "":
            calories_one_elf.append(int(cal))
        else:
            total_calories_per_elf.append(sum(calories_one_elf))
            calories_one_elf.clear()
    return total_calories_per_elf


if __name__ == "__main__":
    calories = calories_per_elf(read_file())
    print(f"Max. calories: {max(calories)}")
    top3 = sorted(calories)[::-1][:3]
    print(f"Sum of top 3: {sum(top3)}")
