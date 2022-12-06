from util import read_file


def test_packet():
    return {
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
    }


def test_message():
    return {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
        "nppdvjthqldpwncqszvftbrmjlhg": 23,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
    }


def get_start_of_packet_pos(datastream: str, length: int) -> int:
    start = 0
    end = start + length
    while datastream[start:end]:
        if len(set(datastream[start:end])) == length:
            return end
        else:
            start += 1
            end += 1


if __name__ == "__main__":

    for datastream, pos in test_packet().items():
        assert get_start_of_packet_pos(datastream, 4) == pos

    for datastream, pos in test_message().items():
        assert get_start_of_packet_pos(datastream, 14) == pos

    for datastream in read_file("input/day6.txt"):
        print(
            f"{get_start_of_packet_pos(datastream, 4)} characters need to be processed before "
            f"the first start-of-packet marker is detected"
        )
        print(
            f"{get_start_of_packet_pos(datastream, 14)} characters need to be processed before "
            f"the first start-of-message marker is detected"
        )
