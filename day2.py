from enum import Enum
from typing import Optional, Tuple
from util import read_file


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


opponent_map = {"A": Choice.ROCK, "B": Choice.PAPER, "C": Choice.SCISSORS}
my_part_one_map = {"X": Choice.ROCK, "Y": Choice.PAPER, "Z": Choice.SCISSORS}
my_part_two_map = {"X": 0, "Y": 3, "Z": 6}


def decode_my_choice(m_key: str, o_key: Optional[str] = None) -> Choice:
    if o_key is None:
        return my_part_one_map[m_key]
    # My choice depends on the opponents choice as I need to choose
    # such that the desired outcome is achieved
    desired_outcome = my_part_two_map[m_key]
    o_choice = opponent_map[o_key]
    m_choice = [mc for mc in Choice if score_outcome(o_choice, mc) == desired_outcome]
    assert len(m_choice) == 1
    return m_choice[0]


def decode_round(encoded_round: str, strategy: str) -> Tuple[Choice, Choice]:
    o_key, m_key = encoded_round.split(" ")
    if strategy == "part_one":
        return opponent_map[o_key], decode_my_choice(m_key)
    elif strategy == "part_two":
        return opponent_map[o_key], decode_my_choice(m_key, o_key)
    else:
        raise ValueError


def score_outcome(opponent: Choice, me: Choice) -> int:
    if opponent == me:
        return 3
    return {
        (Choice.ROCK, Choice.PAPER): 6,
        (Choice.ROCK, Choice.SCISSORS): 0,
        (Choice.PAPER, Choice.ROCK): 0,
        (Choice.PAPER, Choice.SCISSORS): 6,
        (Choice.SCISSORS, Choice.ROCK): 6,
        (Choice.SCISSORS, Choice.PAPER): 0,
    }[opponent, me]


def score_shape(me: Choice) -> int:
    return {Choice.ROCK: 1, Choice.PAPER: 2, Choice.SCISSORS: 3}[me]


def score_round(opponent: Choice, me: Choice) -> int:
    return score_shape(me) + score_outcome(opponent, me)


if __name__ == "__main__":

    # Assert the provided examples are working as expected
    for strategy, scores in zip(["part_one", "part_two"], [[8, 1, 6], [4, 1, 7]]):
        for encoded, score in zip(["A Y", "B X", "C Z"], scores):
            assert score_round(*decode_round(encoded, strategy)) == score

    rounds = read_file("input/day2.txt")
    for strategy in ["part_one", "part_two"]:
        print(strategy)
        print(f"Total score is: {sum([score_round(*decode_round(r, strategy)) for r in rounds])}")
