from util import read_file


def test_data():
    return {
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
    }


def get_start_of_packet_pos(datastream: str) -> int:
    start = 0
    end = start + 4
    while datastream[start:end]:
        if len(set(datastream[start:end])) == 4:
            return end
        else:
            start += 1
            end += 1


if __name__ == "__main__":

    for datastream, pos in test_data().items():
        assert get_start_of_packet_pos(datastream) == pos

    for datastream in read_file("input/day6.txt"):
        print(
            f"{get_start_of_packet_pos(datastream)} characters need to be processed before "
            f"the first start-of-packet marker is detected"
        )
