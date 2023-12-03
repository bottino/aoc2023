import itertools
import re
from dataclasses import dataclass
import pytest

Position = tuple[int, int]


@dataclass
class Number:
    value: int
    positions: list[Position]


def test_get_positions():
    test_case = ["467..114..", "...*......"]
    symbols, numbers, _ = get_positions_from_input(test_case)

    expected_symb = {(1, 3)}
    expected_numbers = [Number(467, [(0, 0), (0, 1), (0, 2)]),
                        Number(114, [(0, 5), (0, 6), (0, 7)])]

    assert symbols == expected_symb
    assert numbers == expected_numbers


def test_sum_example():
    sum_example = sum_part_numbers_from_file("example1.txt")
    assert sum_example == 4361


def test_sum_gear_ratios_example():
    sum_example = sum_gear_ratios_from_file("example1.txt")
    assert sum_example == 467835


def get_positions_from_input(lines: list[str]) -> (set[Position], list[Number], set[Position]):
    symbols = set()
    numbers = []
    stars = []
    for i, line in enumerate(lines):
        symbol_matches = re.finditer(r"[^\d^\.^\n]", line)  # Match everything but dots, digits, or newlines
        for symbol_match in symbol_matches:
            symbol = (i, symbol_match.start())
            symbols.add(symbol)
            if symbol_match.group(0) == "*":
                stars.append(symbol)

        number_matches = re.finditer(r"\d+", line)
        for number_match in number_matches:
            positions = [(i, j) for j in range(*number_match.span())]
            numbers.append(Number(value=int(number_match.group(0)), positions=positions))

    return symbols, numbers, stars


def find_adjacent_numbers(pos: Position, numbers: list[Number]):
    return [n for n in numbers if pos in get_all_neighbors(n)]


def is_part_number(number: Number, symbols: set[Position]) -> bool:
    return any([n in get_all_neighbors(number) for n in symbols])


def sum_part_numbers_from_file(filepath: str) -> int:
    lines = get_lines_from_input_file(filepath)
    symbols, numbers, _ = get_positions_from_input(lines)
    return sum([number.value for number in numbers if is_part_number(number, symbols)])


def sum_gear_ratios_from_file(filepath: str) -> int:
    lines = get_lines_from_input_file(filepath)
    _, numbers, stars = get_positions_from_input(lines)
    return sum([get_gear_ratio(star, numbers) for star in stars])


def get_gear_ratio(star: Position, numbers: list[Number]) -> int:
    adjacents = find_adjacent_numbers(star, numbers)
    if len(adjacents) == 2:
        return adjacents[0].value * adjacents[1].value
    else:
        return 0


def get_all_neighbors(number: Number) -> set[Position]:
    return set(itertools.chain(*[get_neighbors(pos) for pos in number.positions]))


def get_neighbors(pos: Position) -> list[Position]:
    x = pos[0]
    y = pos[1]
    return [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]


def get_lines_from_input_file(filepath: str) -> list[str]:
    return [line for line in open(filepath, "r")]


if __name__ == "__main__":
    print(sum_part_numbers_from_file("input.txt"))
    print(sum_gear_ratios_from_file("input.txt"))
