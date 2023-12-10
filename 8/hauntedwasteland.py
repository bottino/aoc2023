import math
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
    assert traverse_desert_brute_force("example1.txt") == 2
    assert traverse_desert_brute_force("example2.txt") == 6
    assert traverse_desert_brute_force("example3.txt") == 6


def traverse_desert_brute_force(filepath: str) -> int:
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


def get_cycle_length(start_node: Node, instructions: str):
    i = 0
    num_steps = 0
    location = start_node
    traversed = {}
    last_key = None
    while last_key is None:
        direction = instructions[i]
        i = (i + 1) % len(instructions)  # start instructions again if over
        num_steps += 1

        location = location.left if direction == "L" else location.right
        is_z = location.name[-1] == "Z"
        key = (location.name, i)
        if key in traversed:
            last_key = key
        else:
            traversed[key] = (num_steps, is_z)

    zs = [v for v in traversed.values() if v[1] is True]
    first_z = zs[0][0]
    num_zs = len(zs)
    cycle_offset = traversed[last_key][0]
    cycle_length = len(traversed) + 1 - cycle_offset

    # The input is designed very particularly so that the following is true
    assert num_zs == 1
    assert cycle_length == first_z
    return cycle_length


def get_cycle_lengths(filepath: str):
    instructions, nodes = parse_input(filepath)
    locations = [loc for loc in nodes if loc.name[-1] == "A"]
    return [get_cycle_length(loc, instructions) for loc in locations]


def find_number_of_steps_lcm(filepath: str):
    """
    Weirdly, the following is always true in the input I have:
    1. There is only one node that ends with "Z" for each cycle built from one input node
    2. You fall on the "Z" node from the start node after exaclty cycle_length
    It's enough to calculate the least common multiple of the cycle lengths
    """
    return math.lcm(*get_cycle_lengths(filepath))


def parse_input(filepath: str) -> (str, list[Node]):
    lines = [l for l in open(filepath, "r")]
    instructions = lines[0].strip()
    nodes = [re.findall(r"[A-Z0-9]+", line) for line in lines[2:]]
    nodes = {n[0]: (n[1], n[2]) for n in nodes}
    nodes = build_graph(nodes)
    return instructions, nodes


if __name__ == "__main__":
    print(find_number_of_steps_lcm("input.txt"))

