import re
from collections import namedtuple

Race = namedtuple("Race", "t_max record")


def test_parse_input():
    assert parse_input("example.txt") == [(7, 9), (15, 40), (30, 200)]


def test_parse_input_part2():
    assert parse_input_part2("example.txt") == Race(71530, 940200)


def test_get_race_distance():
    races = parse_input("example.txt")
    for hold_time, expected_distance in [(0, 0), (1, 6), (2, 10), (3, 12), (4, 12), (5, 10), (6, 6), (7, 0)]:
        assert get_race_distance(hold_time, races[0]) == expected_distance


def test_get_number_of_winning_combinations():
    races = parse_input("example.txt")
    assert get_number_of_winning_combinations(races[2]) == 9


def test_get_power_winning_combinations():
    races = parse_input("example.txt")
    assert get_power_of_winning_combinations(races) == 288


def test_part_2():
    race = parse_input_part2("input.txt")
    assert get_number_of_winning_combinations(race) == 71503


def parse_input(filepath: str) -> list[Race]:
    lines = [l for l in open(filepath, "r")]
    lines = [[int(n) for n in re.findall("\d+", line)] for line in lines]
    return [Race(*x) for x in zip(*lines)]


def parse_input_part2(filepath: str) -> Race:
    lines = [l for l in open(filepath, "r")]
    lines = [int("".join(re.findall("\d+", line))) for line in lines]
    return Race(*lines)


def get_race_distance(t_hold: int, race: Race) -> int:
    v = t_hold
    t_race = race.t_max - t_hold
    return v * t_race


def get_number_of_winning_combinations(race: Race) -> int:
    w = [get_race_distance(t, race) > race.record for t in range(race.t_max + 1)]
    return sum(w)


def get_power_of_winning_combinations(races):
    power = 1.0
    for race in races:
        power *= get_number_of_winning_combinations(race)
    return power
