from collections import namedtuple

Pipe = namedtuple("Pipe", "x y char")


CONNECTIONS = {
    "F": [(1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "-": [(0, -1), (0, 1)],
    "|": [(-1, 0), (1, 0)],
}


def test_parse_input():
    loop = parse_input("example.txt")
    print("")
    print(loop)
    assert len(loop) == 8


def find_pipes_connected_to_start(start_pos, lines):
    connections = []
    for neighbor in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
        x, y = neighbor[0] + start_pos[0], neighbor[1] + start_pos[1]
        pipe = Pipe(x, y, lines[x][y])
        if (-neighbor[0], -neighbor[1]) in CONNECTIONS[pipe.char]:
            connections.append((pipe, neighbor))
    assert len(connections) == 2
    return connections


def parse_input(filepath: str):
    maze = [line for line in open(filepath, "r")]
    start_pos = [(x, y) for x, line in enumerate(maze) for y, char in enumerate(line) if char == "S"][0]

    start_pipes = find_pipes_connected_to_start(start_pos, maze)

    loop = [start_pipes[0][0]]
    last_connection = start_pipes[0][1]
    while loop[-1].char != "S":
        current = loop[-1]
        connections = set(CONNECTIONS[current.char]) - {last_connection}
        assert len(connections) == 1
        last_connection = list(connections)[0]
        x = current.x + last_connection[0]
        y = current.y + last_connection[1]
        loop.append(Pipe(x=x, y=y, char=maze[x][y]))

    return loop
