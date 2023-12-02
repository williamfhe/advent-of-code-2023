from collections import defaultdict
from typing import Optional

INPUT_FILE = "input.txt"


def is_game_possible(line: str) -> tuple[int, int]:
    game_id_text, game_sets_text = line.split(":")
    game_id = int(game_id_text.split()[1])

    min_cube_counts = defaultdict(int)
    for set_of_cubes in game_sets_text[1:].split("; "):
        color_counts = defaultdict(int)

        for cubes in set_of_cubes.split(", "):
            count, color = cubes.split(" ")
            color_counts[color] += int(count)

        # update the min number of cubes needed of each color for the game
        for color in ("red", "green", "blue"):
            min_cube_counts[color] = max(min_cube_counts[color], color_counts[color])

    power_of_cubes = (
        min_cube_counts["red"] * min_cube_counts["green"] * min_cube_counts["blue"]
    )
    return game_id, power_of_cubes


sum_of_cubes_power = 0
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        # skip empty lines
        line = line.strip()
        if not line:
            continue

        game_id, power_of_cubes = is_game_possible(line)
        sum_of_cubes_power += power_of_cubes

print(sum_of_cubes_power)
