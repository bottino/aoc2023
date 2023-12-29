import re


def test_card():
    line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    assert get_my_winning_numbers(line) == {83, 86, 17, 48}


def test_example_part_1():
    assert sum_of_winning_cards("example.txt") == 13


def test_example_part_2():
    assert sum_number_of_won_cards("example.txt") == 30


def sum_of_winning_cards(filepath: str) -> int:
    lines = [l for l in open(filepath, "r")]
    return sum([get_line_score(line) for line in lines])


def get_line_score(line) -> int:
    num_winnings = len(get_my_winning_numbers(line))
    return 2**(num_winnings - 1) if num_winnings > 0 else 0


def get_my_winning_numbers(line) -> set[int]:
    card, numbers = line.split(":")
    winning, mine = numbers.split("|")
    winning, mine = ({int(w) for w in re.findall(r"\d+", s)} for s in (winning, mine))
    return mine.intersection(winning)


def sum_number_of_won_cards(filepath: str) -> int:
    card_scores = [len(get_my_winning_numbers(l)) for l in open(filepath, "r")]
    card_stack = [1] * len(card_scores)
    for i, score in enumerate(card_scores):
        for j in range(i + 1, i + score + 1):
            card_stack[j] += card_stack[i]
    return sum(card_stack)


if __name__ == "__main__":
    print(sum_of_winning_cards("input.txt"))
    print(sum_number_of_won_cards("input.txt"))




