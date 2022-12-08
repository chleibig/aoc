from collections import defaultdict
from pathlib import PurePath
from typing import Dict, List

from util import read_file


def change_dir(current_path: PurePath, to: str) -> PurePath:
    if to == "..":
        return current_path.parent
    return current_path / to


def parse_dirname(line: str) -> str:
    parts = line.split(" ")
    assert len(parts) == {"$ cd": 3, "dir ": 2}[line[:4]], f"Assuming directory names without whitespace, got '{line}'"
    return parts[-1]


def parse_filesize(line: str) -> int:
    try:
        return int(line.split(" ")[0])
    except ValueError:
        print(f"Can't parse filesize from '{line}'.")
        raise


def infer_filesystem(terminal_output: List[str]) -> Dict[PurePath, List[int]]:
    filesizes_by_dirs = defaultdict(list)
    cwd = PurePath("/")  # no system access and desired handling of rel. and abs. paths
    for line in terminal_output:
        if line.startswith("$"):  # Commands: we only care about `cd`
            assert "cd" in line or "ls" in line, f"Unexpected command '{line}'."
            if "cd" in line:
                cwd = change_dir(cwd, parse_dirname(line))
        elif "dir" in line:  #  Command output from `ls`
            # dirs themselves are empty but need to be tracked because their size might be non-zero via sub-directories
            filesizes_by_dirs[cwd / parse_dirname(line)].append(0)
        else:  # <filesize> <filename>
            filesizes_by_dirs[cwd].append(parse_filesize(line))

    return filesizes_by_dirs


def get_dir_size(filesizes_by_dirs: Dict[PurePath, List[int]], path: PurePath, include_subdirs: bool) -> int:
    if include_subdirs:
        return sum(sum(fs) for p, fs in filesizes_by_dirs.items() if p.is_relative_to(path))
    else:
        return sum(filesizes_by_dirs[path])


def result_part_one(filesizes_by_paths) -> int:
    return sum(
        filter(
            lambda s: s <= 100000,
            [get_dir_size(filesizes_by_paths, p, include_subdirs=True) for p in filesizes_by_paths],
        )
    )


def result_part_two(filesizes_by_dirs) -> int:
    required_space = 30000000 - (70000000 - get_dir_size(filesizes_by_dirs, PurePath("/"), include_subdirs=True))
    for size in sorted([get_dir_size(filesizes_by_dirs, d, True) for d in filesizes_by_dirs]):
        if size >= required_space:
            return size
    raise ValueError(f"No directory found that is large enough to free up {required_space}.")


if __name__ == "__main__":

    terminal_output = read_file("input/test_day7.txt")
    filesizes_by_dirs = infer_filesystem(terminal_output)
    assert get_dir_size(filesizes_by_dirs, PurePath("/a/e"), True) == 584
    assert get_dir_size(filesizes_by_dirs, PurePath("/a"), True) == 94853
    assert get_dir_size(filesizes_by_dirs, PurePath("/d"), True) == 24933642
    assert get_dir_size(filesizes_by_dirs, PurePath("/"), True) == 48381165
    assert result_part_one(filesizes_by_dirs) == 95437
    assert result_part_two(filesizes_by_dirs) == 24933642

    terminal_output = read_file("input/day7.txt")
    filesizes_by_dirs = infer_filesystem(terminal_output)
    print(f"Part one: {result_part_one(filesizes_by_dirs)}")
    print(f"Part two: {result_part_two(filesizes_by_dirs)}")
