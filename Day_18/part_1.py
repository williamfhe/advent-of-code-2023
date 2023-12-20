from typing import Iterator

DIRECTIONS = {"U": (-1, 0), "R": (0, +1), "D": (+1, 0), "L": (0, -1)}


def load_input(input_path: str = "input.txt") -> Iterator[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


def main():
    x, y = 0, 0
    area = 0
    border_size = 0

    # uses the shoelace formula : https://en.wikipedia.org/wiki/Shoelace_formula
    for line in load_input():
        dir_char, size, _ = line.split(" ")
        size = int(size)
        direction = DIRECTIONS[dir_char]

        xx = x + direction[1] * size
        yy = y + direction[0] * size

        area += (y + yy) * (x - xx)
        # keep the total border size because the formula only computes
        # the inner area
        border_size += size
        x, y = xx, yy

    area = int(1 + abs((area + border_size) / 2))
    print(area)


if __name__ == "__main__":
    main()
