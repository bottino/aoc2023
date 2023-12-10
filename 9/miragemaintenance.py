import re
import numpy as np


def test_predicted_values():
    forward, backward = predict_values("example.txt")
    assert forward == [18, 28, 68, -18]
    assert backward == [-3, 0, 5, 3]


def predict_values(filepath: str):
    lines = [re.findall(r"-?\d+", line) for line in open(filepath, "r")]
    predictions = [predict(line) for line in lines]
    return [list(pred) for pred in zip(*predictions)]


def predict(line):
    line = [int(number) for number in line]
    pile = [np.array(line)]
    while any([number != 0 for number in pile[-1]]):
        pile.append(pile[-1][1:] - pile[-1][:-1])

    forward = sum([seq[-1] for seq in pile])
    backward = 0
    for i in range(2, len(pile) + 1):
        backward = pile[-i][0] - backward
    return forward, backward


if __name__ == "__main__":
    f, b = predict_values("input.txt")
    print(sum(f), sum(b))
