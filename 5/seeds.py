import re

Line = tuple[int, int, int]
Map = dict[int, int]


def test_parse_input():
    seeds, maps = parse_input("example.txt")
    assert seeds == [79, 14, 55, 13]
    assert maps[-1][93] == 56
    assert maps[-2][69] == 0
    assert maps[2][57] == 53


def test_location_from_seed():
    assert get_locations_from_file("example.txt") == [82, 43, 86, 35]


def get_locations_from_file(filepath: str):
    print("Parsing input...")
    seeds, maps = parse_input(filepath)
    locations = []
    for i, seed in enumerate(seeds):
        print(f"Seed {i + 1}/{len(seeds)}...")
        locations.append(get_locations_from_seeds(seed, maps))
    return locations


def get_locations_from_seeds(seed: int, maps: list[Map]):
    value = seed
    for map in maps:
        value = map.get(value, value)
    return value


def parse_input(filepath: str) -> (list[int], list[Map]):
    print("Reading file")
    lines = [l for l in open(filepath, "r")]

    print("Reading seeds")
    seeds = [int(num) for num in re.findall(r"\d+", lines[0])]

    print("Reading maps")
    maps = []
    for j, line in enumerate(lines[1:]):
        print(f"Line {j + 1}/{len(lines)}")
        # We found a new map; append a new list
        if line.find("map") != -1:
            maps.append({})

        map_line = [int(num) for num in re.findall(r"\d+", line)]
        if len(map_line) > 0:
            maps[-1].update({map_line[1] + i: map_line[0] + i for i in range(map_line[2])})

    return seeds, maps


if __name__ == "__main__":
    print("part 1")
    print(min(get_locations_from_file("input.txt")))


