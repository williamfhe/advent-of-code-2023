from typing import Optional
import math


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

POSSIBLES_STARTS = ["|", "-", "L", "J", "7", "F"]


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
def walk_the_loop_and_return_its_size_if_it_is_valid(
    maze: MAZE_TYPE, start_row: int, start_col: int
) -> Optional[int]:
    row, col = start_row, start_col

    # define the starting direction
    starting_char = maze[row][col]
    direction = list(DIRECTION_CHANGES[starting_char].values())[0]
    loop_len = 0
    while True:
        if can_continue_in_direction(maze, (row, col), direction):
            row += direction[0]
            col += direction[1]
        else:
            return None

        char_at = maze[row][col]
        direction = DIRECTION_CHANGES[char_at][direction]
        loop_len += 1
        if row == start_row and col == start_col:
            return loop_len


def find_farthest_starting_position(maze: MAZE_TYPE) -> tuple[int, int]:
    start_row, start_col = find_starting_position(maze)

    max_loop_len = 0
    for possible_start in POSSIBLES_STARTS:
        maze[start_row][start_col] = possible_start  # to check for a loop

        loop_len = walk_the_loop_and_return_its_size_if_it_is_valid(
            maze, start_row, start_col
        )
        if loop_len:
            max_loop_len = max(max_loop_len, loop_len)

    return math.ceil(max_loop_len / 2)


def main():
    maze = load_input()
    farthest_position = find_farthest_starting_position(maze)
    print(farthest_position)


if __name__ == "__main__":
    main()
