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


@dataclass(unsafe_hash=True)
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


def compute_beam_movement(contraption: tuple[str], beam: Beam) -> set[Beam]:
    returned_beams = set()

    if not 0 <= beam.row < len(contraption) or not 0 <= beam.col < len(contraption[0]):
        # beam is out of bounds
        return returned_beams

    match contraption[beam.row][beam.col]:
        case ".":
            returned_beams.add(beam)
        case "|":
            if beam.direction in (EAST, WEST):
                returned_beams.add(Beam(beam.row, beam.col, NORTH))
                returned_beams.add(Beam(beam.row, beam.col, SOUTH))
            else:
                returned_beams.add(beam)
        case "-":
            if beam.direction in (NORTH, SOUTH):
                returned_beams.add(Beam(beam.row, beam.col, EAST))
                returned_beams.add(Beam(beam.row, beam.col, WEST))
            else:
                returned_beams.add(beam)
        case "/":
            beam.direction = TILE_TO_DIRECTION["/"][beam.direction]
            returned_beams.add(beam)
        case "\\":
            beam.direction = TILE_TO_DIRECTION["\\"][beam.direction]
            returned_beams.add(beam)

    return returned_beams


def find_energized_tiles_for_start(contraption: tuple[str], starting_beam: Beam) -> int:
    energized_tiles = defaultdict(set)
    continue_looping = True
    beams = {starting_beam}
    while beams and continue_looping:
        new_beams = set()
        continue_looping = False
        for beam in beams:
            if beam.direction not in energized_tiles[(beam.row, beam.col)]:
                # found a tile that was not yet passed in a specific direction
                continue_looping = True
                energized_tiles[(beam.row, beam.col)].add(beam.direction)
            else:
                continue

            beam.row += beam.direction[0]
            beam.col += beam.direction[1]

            ret = compute_beam_movement(contraption, beam)
            new_beams.update(ret)
        beams = new_beams

    return len(energized_tiles) - 1


def main():
    contraption = tuple(load_input())

    max_energized_tiles = 0

    width = len(contraption[0])
    height = len(contraption)
    for col in range(width):
        # top
        max_energized_tiles = max(
            max_energized_tiles,
            find_energized_tiles_for_start(contraption, Beam(-1, col, SOUTH)),
        )
        # bottom
        max_energized_tiles = max(
            max_energized_tiles,
            find_energized_tiles_for_start(contraption, Beam(height, col, NORTH)),
        )

    for row in range(height):
        # left
        max_energized_tiles = max(
            max_energized_tiles,
            find_energized_tiles_for_start(contraption, Beam(row, -1, EAST)),
        )
        # right
        max_energized_tiles = max(
            max_energized_tiles,
            find_energized_tiles_for_start(contraption, Beam(row, width, WEST)),
        )

    print(max_energized_tiles)


if __name__ == "__main__":
    main()
