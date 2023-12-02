from collections import defaultdict

INPUT_FILE = "input.txt"


def is_game_possible(line: str) -> tuple[int, bool]:
    game_id_text, game_sets_text = line.split(":")
    game_id = int(game_id_text.split()[1])

    for set_of_cubes in game_sets_text[1:].split("; "):
        color_counts = defaultdict(int)
        for cubes in set_of_cubes.split(", "):
            count, color = cubes.split(" ")
            color_counts[color] += int(count)

            if color == "red" and color_counts.get("red") > 12:
                return game_id, False
            if color == "green" and color_counts.get("green") > 13:
                return game_id, False
            if color == "blue" and color_counts.get("blue") > 14:
                return game_id, False

    return game_id, True


possible_games_id_sum = 0
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        # skip empty lines
        line = line.strip()
        if not line:
            continue

        game_id, possible = is_game_possible(line)
        if possible:
            possible_games_id_sum += game_id

print(possible_games_id_sum)
