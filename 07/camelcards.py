import re
from collections import namedtuple
from enum import Enum


Hand = namedtuple("Hand", "cards bid")


class Type(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_KIND = 5
    FIVE_OF_KIND = 6


CARDS = ["J", *[str(i) for i in range(2, 10)], "T", "Q", "K", "A"]
CARD_STRENGTH = {c: i for i, c in enumerate(CARDS)}


def test_parse_input():
    assert parse_input("example.txt")[0] == ("32T3K", 765)


def test_get_hand_type():
    hands = parse_input("example.txt")
    assert [get_hand_type(hand) for hand in hands] == [
        Type.ONE_PAIR,
        Type.FOUR_OF_KIND,
        Type.TWO_PAIRS,
        Type.FOUR_OF_KIND,
        Type.FOUR_OF_KIND,
    ]


def test_get_hand_type_all():
    hands = ["JJJJJ", "JJTJJ", "23232", "2221T", "99242", "9TKJA", "AKAQJ", "23456"]
    hands = [Hand(h, 0) for h in hands]
    assert [get_hand_type(hand) for hand in hands] == [
        Type.FIVE_OF_KIND,
        Type.FIVE_OF_KIND,
        Type.FULL_HOUSE,
        Type.THREE_OF_KIND,
        Type.TWO_PAIRS,
        Type.ONE_PAIR,
        Type.THREE_OF_KIND,
        Type.HIGH_CARD,
    ]


def test_get_total_winnings():
    assert get_total_winnings("example.txt") == 5905


def test_input_same_hands():
    hands = parse_input("input.txt")
    num_hands = len(hands)
    cards = {"".join(sorted(hand.cards)) for hand in hands}
    assert len(cards) == num_hands


def get_hand_type(hand: Hand) -> Type:
    # Handle exception
    if hand.cards == "JJJJJ":
        return Type.FIVE_OF_KIND

    cards = [c for c in hand.cards if c != "J"]
    card_nums = {c: 0 for c in cards}
    for c in cards:
        card_nums[c] += 1

    num_jokers = sum([c == "J" for c in hand.cards])
    most_frequent_card = sorted(
        card_nums.items(), key=lambda item: item[1], reverse=True
    )[0][0]
    card_nums[most_frequent_card] += num_jokers

    if max(card_nums.values()) == 5:
        return Type.FIVE_OF_KIND
    elif max(card_nums.values()) == 4:
        return Type.FOUR_OF_KIND
    elif max(card_nums.values()) == 3:
        if min(card_nums.values()) == 2:
            return Type.FULL_HOUSE
        else:
            return Type.THREE_OF_KIND
    elif max(card_nums.values()) == 2:
        if len(card_nums) == 3:
            return Type.TWO_PAIRS
        else:
            return Type.ONE_PAIR
    else:
        return Type.HIGH_CARD


def get_total_winnings(filepath: str):
    hands = parse_input(filepath)
    hand_values = [(hand, get_hand_value(hand)) for hand in hands]
    hand_values.sort(key=lambda h: h[1])
    winnings = [h[0].bid * (i + 1) for i, h in enumerate(hand_values)]
    return sum(winnings)


def get_hand_value(hand: Hand) -> int:
    hand_type = get_hand_type(hand)
    strengths = [CARD_STRENGTH[c] for c in hand.cards]
    strengths.reverse()
    return sum([v * 100**i for i, v in enumerate([*strengths, hand_type.value])])


def parse_input(filepath: str) -> list[Hand]:
    lines = [l for l in open(filepath, "r")]
    lines = [re.findall("\w+", line) for line in lines]
    return [Hand(line[0], int(line[1])) for line in lines]


if __name__ == "__main__":
    print(get_total_winnings("input.txt"))
