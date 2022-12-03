from enum import Enum
from typing import Optional, Tuple
from util import read_file


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


opponent_shape = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}


def decode_my_shape(m_key: str, o_key: Optional[str] = None) -> Shape:
    if o_key is None:
        # My chosen shape is static
        return {"X": Shape.ROCK, "Y": Shape.PAPER, "Z": Shape.SCISSORS}[m_key]
    else:
        # Brute force the play to achieve the desired outcome
        desired_outcome = {"X": Outcome.LOSS, "Y": Outcome.DRAW, "Z": Outcome.WIN}[m_key]
        for my_shape in Shape:
            if play(my_shape, opponent_shape[o_key]) == desired_outcome:
                return my_shape


def decode_round(encoded_round: str, strategy: str) -> Tuple[Shape, Shape]:
    o_key, m_key = encoded_round.split(" ")
    if strategy == "part_one":
        return decode_my_shape(m_key), opponent_shape[o_key]
    elif strategy == "part_two":
        return decode_my_shape(m_key, o_key), opponent_shape[o_key]
    else:
        raise ValueError


def play(me: Shape, against: Shape) -> Outcome:
    if me == against:
        return Outcome.DRAW
    return {
        (Shape.SCISSORS, Shape.ROCK): Outcome.LOSS,
        (Shape.ROCK, Shape.PAPER): Outcome.LOSS,
        (Shape.PAPER, Shape.SCISSORS): Outcome.LOSS,
    }.get((me, against), Outcome.WIN)


def score_round(me: Shape, against: Shape) -> int:
    return me.value + play(me, against).value


if __name__ == "__main__":

    # Assert the provided examples are working as expected
    for strategy, scores in zip(["part_one", "part_two"], [[8, 1, 6], [4, 1, 7]]):
        for encoded, score in zip(["A Y", "B X", "C Z"], scores):
            assert score_round(*decode_round(encoded, strategy)) == score

    rounds = read_file("input/day2.txt")
    for strategy in ["part_one", "part_two"]:
        print(strategy)
        print(f"Total score is: {sum([score_round(*decode_round(r, strategy)) for r in rounds])}")
