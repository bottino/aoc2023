import re
import pytest


number_dict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


example_files = [
    ("example.txt", 142),
    ("example2.txt", 281),
    ("example3.txt", 55 + 67 + 96 + 16 + 45 + 66 + 97)
]

@pytest.mark.parametrize("example,expected", example_files)
def test_example(example, expected):
    assert get_total_calibration(example) == expected

test_data = [
    ("1wbc2", 12),
    ("pqr3stu8vwx", 38),
    ("a1b2c3d45f", 15),
    ("treb7uchet", 77),
    ("two1nine", 29),
    ("4nineeightseven2", 42),
    ("fjzoneight", 18),
]
@pytest.mark.parametrize("line,expected", test_data)
def test_find_line(line, expected):
    assert get_calibration_for_line(line) == expected


def get_calibration_for_line(line: str) -> int:
    spelled_out_pattern = r"|".join(number_dict.keys())
    matches = re.findall(r"(?=(\d|" + spelled_out_pattern + r"))", line)  # find all values, each in a separate match
    matches = [number_dict.get(m, m) for m in matches]  # replace by dict value if exists (for text numbers)
    return 10 * int(matches[0]) + int(matches[-1])


def get_total_calibration(path: str) -> int:
    sum_calibration = 0
    with open(path, "r") as f:
        for line in f:
            sum_calibration += get_calibration_for_line(line)

    return sum_calibration


if __name__ == "__main__":
    print(get_total_calibration("input.txt"))




