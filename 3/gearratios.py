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
    symbols, numbers = get_positions_from_input(test_case)

    expected_symb = {(1, 3)}
    expected_numbers = [Number(467, [(0, 0), (0, 1), (0, 2)]),
                        Number(114, [(0, 5), (0, 6), (0, 7)])]

    assert symbols == expected_symb
    assert numbers == expected_numbers


def test_sum_example():
    sum_example = sum_part_numbers_from_file("example1.txt")
    assert sum_example == 4361


def get_positions_from_input(lines: list[str]) -> (set[Position], list[Number]):
    symbols = set()
    numbers = []
    for i, line in enumerate(lines):
        symbol_matches = re.finditer(r"[^\d^\.^\n]", line)  # Match everything but dots, digits, or newlines
        for symbol_match in symbol_matches:
            symbols.add((i, symbol_match.start()))

        number_matches = re.finditer(r"\d+", line)
        for number_match in number_matches:
            positions = [(i, j) for j in range(*number_match.span())]
            numbers.append(Number(value=int(number_match.group(0)), positions=positions))

    return symbols, numbers


def is_part_number(number: Number, symbols: set[Position]) -> bool:
    for digit in number.positions:
        neighbors = get_neighbors(digit)
        for neighbor in neighbors:
            if neighbor in symbols:
                return True

    return False


def sum_part_numbers_from_file(filepath: str) -> int:
    lines = get_lines_from_input_file(filepath)
    symbols, numbers = get_positions_from_input(lines)
    sum_part_numbers = 0
    for number in numbers:
        if is_part_number(number, symbols):
            sum_part_numbers += number.value
    return sum_part_numbers


def get_neighbors(pos: Position) -> list[Position]:
    x = pos[0]
    y = pos[1]
    return [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]


def get_lines_from_input_file(filepath: str) -> list[str]:
    with open(filepath, "r") as f:
        lines = [line for line in f]
    return lines


if __name__ == "__main__":
    print(sum_part_numbers_from_file("input.txt"))
