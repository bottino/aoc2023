import re
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    name: str
    left: Optional[Any] = None
    right: Optional[Any] = None


def test_parse_input():
    instructions, nodes = parse_input("example3.txt")
    assert instructions == "LR"
    print(nodes)
    assert nodes[0].name == "11A"
    assert nodes[0].left.name == "11B"
    assert nodes[0].right.name == "XXX"


def test_traverse_desert():
    assert traverse_desert("example1.txt") == 2
    assert traverse_desert("example2.txt") == 6
    assert traverse_desert("example3.txt") == 6
    assert traverse_desert("input.txt") == 6


def traverse_desert(filepath: str) -> int:
    instructions, nodes = parse_input(filepath)
    locations = [loc for loc in nodes if loc.name[-1] == "A"]
    i = 0
    num_steps = 0
    while any([loc.name[-1] != "Z" for loc in locations]):
        direction = instructions[i]
        i = (i + 1) % len(instructions)  # start instructions again if over
        num_steps += 1

        locations = [loc.left if direction == "L" else loc.right for loc in locations]

    return num_steps


def build_graph(node_lines) -> list[Node]:
    nodes = {key: Node(key) for key in node_lines.keys()}
    for key, node in nodes.items():
        node.left = nodes[node_lines[key][0]]
        node.right = nodes[node_lines[key][1]]
    return [n for n in nodes.values()]


def parse_input(filepath: str) -> (str, list[Node]):
    lines = [l for l in open(filepath, "r")]
    instructions = lines[0].strip()
    nodes = [re.findall(r"[A-Z0-9]+", line) for line in lines[2:]]
    nodes = {n[0]: (n[1], n[2]) for n in nodes}
    print("")
    print(nodes)
    nodes = build_graph(nodes)
    return instructions, nodes


if __name__ == "__main__":
    print(traverse_desert("input.txt"))

