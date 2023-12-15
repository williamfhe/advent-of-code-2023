PLATFORM_TYPE = list[list[str]]


def load_input(input_path: str = "input.txt") -> PLATFORM_TYPE:
    with open(input_path, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f if line]


def find_place_for_rock(platform: PLATFORM_TYPE, rock_row: int, rock_col: int) -> int:
    best_row = rock_row
    for r in range(rock_row - 1, -1, -1):
        if platform[r][rock_col] == ".":
            best_row = r
        else:
            break

    return best_row


def tilt_north(platform: PLATFORM_TYPE) -> PLATFORM_TYPE:
    for r, row in enumerate(platform):
        for c, cell in enumerate(row):
            if cell == "O":
                new_row = find_place_for_rock(platform, r, c)
                platform[r][c] = "."
                platform[new_row][c] = "O"


def display_platform(platform: PLATFORM_TYPE):
    for line in platform:
        print("".join(line))


def compute_load(platform: PLATFORM_TYPE) -> int:
    total_load = 0
    for r, row in enumerate(platform):
        for cell in row:
            if cell == "O":
                total_load += len(platform) - r
    return total_load


def main():
    platform = load_input()
    tilt_north(platform)
    # display_platform(platform)
    total_load = compute_load(platform)
    print(total_load)


if __name__ == "__main__":
    main()
