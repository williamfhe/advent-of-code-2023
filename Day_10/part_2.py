from typing import Optional
from collections import defaultdict


MAZE_TYPE = list[list[str]]
VecI2 = tuple[int, int]

NORTH = (-1, 0)
EAST = (0, +1)
SOUTH = (+1, 0)
WEST = (0, -1)


DIRECTION_CHANGES = {
    "|": {NORTH: NORTH, SOUTH: SOUTH},
    "-": {EAST: EAST, WEST: WEST},
    "L": {SOUTH: EAST, WEST: NORTH},
    "J": {EAST: NORTH, SOUTH: WEST},
    "7": {EAST: SOUTH, NORTH: WEST},
    "F": {NORTH: EAST, WEST: SOUTH},
    ".": {},  # no new direction
}


# the only value for "S" that makes the loop possible
# computed in part 1
STARTING_MAZE_CHAR = "|"


def load_input(input_path: str = "input.txt") -> MAZE_TYPE:
    maze = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            maze.append(list(line))

    return maze


def can_continue_in_direction(
    maze: MAZE_TYPE, position: VecI2, direction: VecI2
) -> bool:
    new_row, new_col = position[0] + direction[0], position[1] + direction[1]

    # check if out of bound
    if not 0 <= new_row < len(maze):
        return False

    if not 0 <= new_col < len(maze[new_row]):
        return False

    maze_char = maze[new_row][new_col]
    if direction not in DIRECTION_CHANGES[maze_char]:
        return False

    return True


def find_starting_position(maze: MAZE_TYPE) -> VecI2:
    for i, row in enumerate(maze):
        if "S" in row:
            return i, row.index("S")

    raise ValueError("Invalid maze, no 'S' found")


# Didn't find a short and explicit name
def walk_the_loop_and_return_all_border_positions(
    maze: MAZE_TYPE, start_row: int, start_col: int
) -> set[VecI2]:
    row, col = start_row, start_col

    # define the starting direction
    maze[row][col] = STARTING_MAZE_CHAR
    direction = list(DIRECTION_CHANGES[STARTING_MAZE_CHAR].values())[0]

    loop_borders = set()

    while True:
        row += direction[0]
        col += direction[1]

        char_at = maze[row][col]
        direction = DIRECTION_CHANGES[char_at][direction]

        loop_borders.add((row, col))
        if row == start_row and col == start_col:
            return loop_borders


def compute_count_of_enclosed_tiles(maze: MAZE_TYPE) -> int:
    start_row, start_col = find_starting_position(maze)
    maze[start_row][start_col] = STARTING_MAZE_CHAR

    border_positions = walk_the_loop_and_return_all_border_positions(
        maze, start_row, start_col
    )

    # uses a derivated way from this https://en.wikipedia.org/wiki/Point_in_polygon
    # we use a boolean instead of an odd/even integer to check if we are in the maze (polygon)
    enclosed_count = 0
    for row in range(len(maze)):
        is_enclosed = False
        for col in range(len(maze[row])):
            if (row, col) in border_positions:
                # Ignore F7 but could also have checked for "|F7" and ignored JL
                if maze[row][col] in "|JL":
                    is_enclosed = not is_enclosed
            else:
                if is_enclosed:
                    enclosed_count += 1

    return enclosed_count


def main():
    maze = load_input()
    enclosed_tiles_count = compute_count_of_enclosed_tiles(maze)
    print(enclosed_tiles_count)


if __name__ == "__main__":
    main()
