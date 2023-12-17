from dataclasses import dataclass
from collections import defaultdict

NORTH = (-1, 0)
EAST = (0, +1)
SOUTH = (+1, 0)
WEST = (0, -1)

TILE_TO_DIRECTION = {
    "/": {NORTH: EAST, WEST: SOUTH, SOUTH: WEST, EAST: NORTH},
    "\\": {NORTH: WEST, WEST: NORTH, SOUTH: EAST, EAST: SOUTH},
}


@dataclass
class Beam:
    row: int
    col: int
    direction: tuple[int, int]


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def display_energized_tiles(
    energized_tiles: set[tuple[int, int]], width: int, height: int
):
    for row in range(height):
        for col in range(width):
            if (row, col) in energized_tiles:
                print("#", end="")
            else:
                print(".", end="")
        print()


def main():
    contraption = load_input()
    beams = [Beam(0, -1, EAST)]

    width, height = len(contraption[0]), len(contraption)

    # contains tile => direction
    energized_tiles = defaultdict(set)
    continue_looping = True
    while beams and continue_looping:
        new_beams = []

        continue_looping = False
        for beam in beams:
            if beam.direction not in energized_tiles[(beam.row, beam.col)]:
                # found a tile that was not yet passed in a specific direction
                continue_looping = True
                energized_tiles[(beam.row, beam.col)].add(beam.direction)
            else:
                continue

            # new coordinates
            beam.row += beam.direction[0]
            beam.col += beam.direction[1]

            if not 0 <= beam.row < height or not 0 <= beam.col < width:
                # beam is out of bounds
                continue

            match contraption[beam.row][beam.col]:
                case ".":
                    new_beams.append(beam)
                case "|":
                    if beam.direction in (EAST, WEST):
                        new_beams.append(Beam(beam.row, beam.col, NORTH))
                        new_beams.append(Beam(beam.row, beam.col, SOUTH))
                    else:
                        new_beams.append(beam)
                case "-":
                    if beam.direction in (NORTH, SOUTH):
                        new_beams.append(Beam(beam.row, beam.col, EAST))
                        new_beams.append(Beam(beam.row, beam.col, WEST))
                    else:
                        new_beams.append(beam)
                case "/":
                    beam.direction = TILE_TO_DIRECTION["/"][beam.direction]
                    new_beams.append(beam)
                case "\\":
                    beam.direction = TILE_TO_DIRECTION["\\"][beam.direction]
                    new_beams.append(beam)

        beams = new_beams

    # display_energized_tiles(set(energized_tiles.keys()), width, height)

    # -1 because there is (0, -1) that should be ignored
    print(len(energized_tiles) - 1)


if __name__ == "__main__":
    main()
