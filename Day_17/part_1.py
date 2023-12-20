from queue import PriorityQueue
from typing import Optional


NORTH = (-1, 0)
EAST = (0, +1)
SOUTH = (+1, 0)
WEST = (0, -1)


DIRECTIONS = (NORTH, EAST, SOUTH, WEST)

CellLocation = tuple[int, int]


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def parse_input(input_path: str = "input.txt") -> list[list[int]]:
    city_map = []
    for line in load_input(input_path):
        city_line = []
        for loss_str in line:
            city_line.append(int(loss_str))
        city_map.append(city_line)
    return city_map


def compute_path_with_least_loss(
    city_map: list[list[int]],
    start: CellLocation,
    destination: CellLocation,
) -> int:
    to_check = PriorityQueue()
    to_check.put((0, start, None))

    move_costs = {}

    width = len(city_map[0])
    height = len(city_map)

    while not to_check.empty():
        heatloss, current_cell, source_direction = to_check.get()

        if current_cell == destination:
            return heatloss

        for direction_index in range(4):
            move_heatloss = heatloss
            if source_direction is not None:
                if direction_index % 2 == source_direction % 2:
                    continue
            direction = DIRECTIONS[direction_index]

            for move in range(1, 4):
                neighbour = (
                    current_cell[0] + direction[0] * move,
                    current_cell[1] + direction[1] * move,
                )

                if not 0 <= neighbour[0] < height or not 0 <= neighbour[1] < width:
                    break

                move_heatloss += city_map[neighbour[0]][
                    neighbour[1]
                ]  # add neighbour heatloss

                cache_key = (neighbour, direction_index)
                if cache_key in move_costs:
                    # already found a move that costs less
                    if move_costs[cache_key] <= move_heatloss:
                        continue

                move_costs[cache_key] = move_heatloss
                to_check.put((move_heatloss, neighbour, direction_index))

    raise ValueError("Could not find destination")


def main():
    city_map = parse_input()
    start = (0, 0)
    destination = (len(city_map) - 1, len(city_map[0]) - 1)
    heat_loss = compute_path_with_least_loss(city_map, start, destination)
    print(f"{heat_loss=}")


if __name__ == "__main__":
    main()
