import math
import re
from collections import namedtuple

Race = namedtuple("Race", "t_max record")


def test_parse_input():
    assert parse_input_part1("example.txt") == [(7, 9), (15, 40), (30, 200)]


def test_parse_input_part2():
    assert parse_input_part2("example.txt") == Race(71530, 940200)


def test_get_number_of_winning_combinations():
    races = parse_input_part1("example.txt")
    assert get_number_of_winning_combinations(races[2]) == 9


def test_get_power_winning_combinations():
    races = parse_input_part1("example.txt")
    assert get_power_of_winning_combinations(races) == 288


def test_part_2():
    race = parse_input_part2("example.txt")
    assert get_number_of_winning_combinations(race) == 71503


def parse_input_part1(filepath: str) -> list[Race]:
    lines = [l for l in open(filepath, "r")]
    lines = [[int(n) for n in re.findall("\d+", line)] for line in lines]
    return [Race(*x) for x in zip(*lines)]


def parse_input_part2(filepath: str) -> Race:
    lines = [l for l in open(filepath, "r")]
    lines = [int("".join(re.findall("\d+", line))) for line in lines]
    return Race(*lines)


def get_number_of_winning_combinations(race: Race) -> int:
    roots = find_roots_for_time_equation(race)
    return (roots[1] - roots[0]) + 1


def find_roots_for_time_equation(race: Race):
    # L'equation a resoudre est t * (t_max - t) = record => t * t - t_max * t + record = 0
    a = 1.0
    b = float(-race.t_max)
    c = float(race.record)
    delta = b * b - 4.0 * a * c
    roots = [(-b + factor * math.sqrt(delta)) / (2.0 * a) for factor in (-1, 1)]

    # The lowest number of the winning range must be the integer just above the smaller root, the highest number just
    # below the higher root
    return (int(roots[0]) + 1, int(roots[1] - 0.00001))


def get_power_of_winning_combinations(races):
    power = 1.0
    for race in races:
        power *= get_number_of_winning_combinations(race)
    return power


if __name__ == "__main__":
    # Part 1
    races_part1 = parse_input_part1("input.txt")
    print(get_power_of_winning_combinations(races_part1))

    # Part 2
    race_part2 = parse_input_part2("input.txt")
    print(get_number_of_winning_combinations(race_part2))
