from enum import Enum
from typing import Tuple
from util import read_file


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


opponent_map = {"A": Choice.ROCK, "B": Choice.PAPER, "C": Choice.SCISSORS}
my_map = {"X": Choice.ROCK, "Y": Choice.PAPER, "Z": Choice.SCISSORS}


def decode_round(encoded_round: str) -> Tuple[Choice, Choice]:
    o_choice, m_choice = encoded_round.split(" ")
    return opponent_map[o_choice], my_map[m_choice]


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

    assert score_round(*decode_round("A Y")) == 8
    assert score_round(*decode_round("B X")) == 1
    assert score_round(*decode_round("C Z")) == 6

    rounds = read_file("input_day2.txt")
    print(f"Total score is: {sum([score_round(*decode_round(r)) for r in rounds])}")
