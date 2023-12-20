from typing import Iterator


DIRECTIONS = ((0, +1), (+1, 0), (0, -1), (-1, 0))


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
        _, _, hexcode = line.split(" ")

        hexcode = hexcode[2:-1]
        size = int(hexcode[:-1], base=16)
        dir_index = int(hexcode[-1])

        direction = DIRECTIONS[dir_index]

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
