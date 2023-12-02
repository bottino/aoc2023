import dataclasses
import re
from dataclasses import dataclass

import pytest


@dataclass
class Limits:
    red: int
    green: int
    blue: int


@dataclass
class Trial:
    red: int = 0
    green: int = 0
    blue: int = 0

    def is_possible(self, limits: Limits):
        return self.red <= limits.red and self.green <= limits.green and self.blue <= limits.blue


@dataclass
class Game:
    index: int
    trials: list[Trial]


def test_sum_indices():
    sum_indices = get_sum_of_indices_for_possible_games("example1.txt")
    assert sum_indices == 8


def test_sum_powers():
    sum_powers = get_power_of_cubes_for_all_games("example1.txt")
    assert sum_powers == 2286


def test_min_set():
    line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    game = read_game(line)
    assert get_min_set_of_cubes(game) == {"red": 4, "green": 2, "blue": 6}


def test_is_game_possible():
    line = "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    game = read_game(line)
    limits = Limits(red=12, green=13, blue=14)
    assert is_game_possible(game, limits) is True


def test_read_game():
    line = "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    game = read_game(line)
    expected = Game(2, [
        Trial(red=0, green=2, blue=1),
        Trial(red=1, green=3, blue=4),
        Trial(red=0, green=1, blue=1),
    ])
    assert game == expected


def read_game(line: str) -> Game:
    m = re.match(r"^Game (\d+):(.+)", line)
    index = int(m.groups()[0])
    game = m.groups()[1]

    trial_matches = re.findall(r"((?: \d+ (?:red|green|blue),?)+;?)", game)
    trials = []
    for t in trial_matches:
        color_regex = r"(\d+) (red|green|blue),?"
        color_matches = re.finditer(color_regex, t)
        trial = {m.groups()[1]: int(m.groups()[0]) for m in color_matches}
        trials.append(Trial(**trial))

    return Game(index=index, trials=trials)


def is_game_possible(game: Game, limits: Limits):
    is_possible = True
    for trial in game.trials:
        is_possible = is_possible and trial.is_possible(limits)
    return is_possible


def get_sum_of_indices_for_possible_games(filepath: str):
    limits = Limits(red=12, green=13, blue=14)
    sum_indices = 0
    with open(filepath, "r") as f:
        for line in f:
            game = read_game(line)
            if is_game_possible(game, limits):
                sum_indices += game.index

    return sum_indices


def get_power_of_cubes_for_all_games(filepath: str):
    sum_powers = 0
    with open(filepath, "r") as f:
        for line in f:
            game = read_game(line)
            min_set = get_min_set_of_cubes(game)
            sum_powers += min_set["red"] * min_set["green"] * min_set["blue"]

    return sum_powers


def get_min_set_of_cubes(game: Game):
    game_dict = dataclasses.asdict(game)
    min_limits = {}
    for color in ["red", "green", "blue"]:
        min_limits[color] = max([t[color] for t in game_dict["trials"]])
    return min_limits


if __name__ == "__main__":
    print(get_sum_of_indices_for_possible_games("input.txt"))
    print(get_power_of_cubes_for_all_games("input.txt"))
