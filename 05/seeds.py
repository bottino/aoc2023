import re

import pytest

Line = tuple[int, int, int]
Range = (int, int)
Map = list[tuple[Range, int]]


input_data = [
    ( (0, 10), (3, 5), 3, ([(6, 8)], [(0, 2), (6, 10)]) ),
    ( (0, 10), (12, 15), 3, ([], [(0, 10)]) ),
    ( (0, 10), (0, 15), 3, ([(3, 13)], []) ),
]


@pytest.mark.parametrize("r,split,delta,expected", input_data)
def test_get_split_ranges(r, split, delta, expected):
    assert get_split_ranges(r, split, delta) == expected


def test_parse_input():
    seeds, maps = parse_input("example.txt")
    assert seeds == [(79, 92), (55, 67)]
    assert maps[-1] == [((56, 92), 4), ((93, 96), -37)]


def test_locations():
    seeds, maps = parse_input("input.txt")
    locations = get_locations_ranges_from_seeds(seeds, maps)
    assert min([l[0] for l in locations]) == 46


def get_locations_ranges_from_seeds(seeds: list[Range], maps: list[Map]) -> list[Range]:
    ranges = seeds
    for m in maps:
        ranges = split_ranges_recursively(ranges, m, [])
    return ranges


def split_ranges_recursively(input_ranges: list[Range], split_map: Map, output_ranges: list[Range]) -> list[Range]:
    new_input_ranges = []
    for r in input_ranges:
        filtered, unfiltered = get_split_ranges(r, split_map[0][0], split_map[0][1])
        new_input_ranges += unfiltered
        output_ranges += filtered
    split_map = split_map[1:]  # remove first element from the list
    if len(new_input_ranges) > 0 and len(split_map) > 0:
        return split_ranges_recursively(new_input_ranges, split_map, output_ranges)
    else:
        return output_ranges + new_input_ranges


def get_split_ranges(r: Range, split: Range, delta: int) -> (list[Range], list[Range]):
    """
    Returns (filtered_range, unfiltered_ranges). The first is the portion of the range that has been
    filtered by `split`. The unfiltered was untouched by the split range. The first list has 0 or 1 element,
    the second 0, 1, or 2
    """
    # Early return if the splitting range doesn't intersect
    if split[1] < r[0] or split[0] > r[1]:
        return [], [r]

    # Case where the split range is larger than the whole range
    if split[0] <= r[0] and split[1] >= r[1]:
        return [(r[0] + delta, r[1] + delta)], []

    # Case where the split range is on the left
    if split[0] <= r[0] and split[1] < r[1]:
        return [(r[0] + delta, split[1] + delta)], [(split[1] + 1, r[1])]

    # Case where the split range is on the right
    if split[0] > r[0] and split[1] >= r[1]:
        return [(split[0] + delta, r[1] + delta)], [(r[0], split[0] - 1)]

    # Case where the split range is in the middle
    if split[0] > r[0] and split[1] < r[1]:
        return [(split[0] + delta, split[1] + delta)], [(r[0], split[0] - 1), (split[1] + 1, r[1])]


def parse_input(filepath: str) -> (list[Range], list[Map]):
    lines = [l for l in open(filepath, "r")]
    seeds = [int(num) for num in re.findall(r"\d+", lines[0])]
    seeds = [(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2)]

    maps = []
    for line in lines[1:]:
        # We found a new map; append a new list
        if line.find("map") != -1:
            maps.append([])

        map_line = [int(num) for num in re.findall(r"\d+", line)]
        if len(map_line) > 0:
            delta = map_line[0] - map_line[1]
            start = map_line[1]
            end = map_line[1] + map_line[2] - 1
            maps[-1].append(((start, end), delta))

    return seeds, maps


if __name__ == "__main__":
    seeds, maps = parse_input("input.txt")
    locations = get_locations_ranges_from_seeds(seeds, maps)
    print(min([l[0] for l in locations]))


