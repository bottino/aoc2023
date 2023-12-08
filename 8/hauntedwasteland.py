import re
from collections import namedtuple

Node = namedtuple("Node", "left right")


def test_parse_input():
    instructions, nodes = parse_input("example2.txt")
    assert instructions == "LLR"
    print(nodes)
    assert nodes["AAA"] == ("BBB", "BBB")
    assert nodes["ZZZ"] == ("ZZZ", "ZZZ")


def test_traverse_desert():
    assert traverse_desert("example1.txt") == 2
    assert traverse_desert("example2.txt") == 6
    assert traverse_desert("input.txt") == 12643


def traverse_desert(filepath: str) -> int:
    instructions, nodes = parse_input(filepath)
    location = "AAA"
    i = 0
    num_steps = 0
    while location != "ZZZ":
        direction = instructions[i]
        i = (i + 1) % len(instructions)  # start instructions again if over
        num_steps += 1
        location = nodes[location].left if direction == "L" else nodes[location].right

    return num_steps


def parse_input(filepath: str) -> (str, dict[str, Node]):
    lines = [l for l in open(filepath, "r")]
    instructions = lines[0].strip()
    nodes = [re.findall(r"[A-Z]+", line) for line in lines[2:]]
    nodes = {n[0]: Node(n[1], n[2]) for n in nodes}
    return instructions, nodes

