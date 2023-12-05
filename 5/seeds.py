import re

Line = tuple[int, int, int]
Map = dict[int, dict[str, int]]


def test_parse_input():
    seeds, maps = parse_input("example.txt")
    assert seeds == [79, 14, 55, 13]
    for test in [(-1, 93, 56), (-2, 69, 0), (2, 57, 53)]:
        assert get_value_from_map(test[1], maps[test[0]]) == test[2]


def get_value_from_map(x: int, map: Map) -> int:
    for k in map.keys():
        if x - k >= 0:
            if x < k + map[k]["range"]:
                return x + map[k]["delta"]

    return x


def test_location_from_seed():
    assert get_locations_from_file("example.txt") == [82, 43, 86, 35]


def get_locations_from_file(filepath: str):
    seeds, maps = parse_input(filepath)
    return [get_locations_from_seeds(seed, maps) for seed in seeds]


def get_locations_from_seeds(seed: int, maps: list[Map]):
    value = seed
    for map in maps:
        value = get_value_from_map(value, map)
    return value


def parse_input(filepath: str) -> (list[int], list[Map]):
    lines = [l for l in open(filepath, "r")]
    seeds = [int(num) for num in re.findall(r"\d+", lines[0])]

    maps = []
    for line in lines[1:]:
        # We found a new map; append a new list
        if line.find("map") != -1:
            maps.append({})

        map_line = [int(num) for num in re.findall(r"\d+", line)]
        if len(map_line) > 0:
            maps[-1][map_line[1]] = {"delta": map_line[0] - map_line[1], "range": map_line[2]}

    return seeds, maps


if __name__ == "__main__":
    print(min(get_locations_from_file("input.txt")))


