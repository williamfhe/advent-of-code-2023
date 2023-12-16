from typing import Iterator
from collections import defaultdict


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def parse_input(input_path: str = "input.txt") -> Iterator[str]:
    for line in load_input(input_path):
        for splited in line.split(","):
            yield splited


def compute_hash(string: str) -> int:
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256

    return value


def main():
    boxes = defaultdict(dict)

    for p in parse_input():
        if "-" in p:
            label = p[:-1]
            h = compute_hash(label)
            boxes[h].pop(label, None)
        else:
            label, lens = p.split("=")
            lens = int(lens)
            h = compute_hash(label)
            boxes[h][label] = lens

    total = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses.values()):
            total += (box + 1) * (i + 1) * lens

    print(total)


if __name__ == "__main__":
    main()
