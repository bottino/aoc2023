import re
import numpy as np


def test_predicted_values():
    values = predict_values("example.txt")
    assert values == [18, 28, 68, -18]


def predict_values(filepath: str):
    lines = [re.findall(r"-?\d+", line) for line in open(filepath, "r")]
    return [predict(line) for line in lines]


def predict(line):
    line = [int(number) for number in line]
    pile = [np.array(line)]
    while any([number != 0 for number in pile[-1]]):
        pile.append(pile[-1][1:] - pile[-1][:-1])

    return sum([seq[-1] for seq in pile])


if __name__ == "__main__":
    print(sum(predict_values("input.txt")))
