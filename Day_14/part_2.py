PLATFORM_TYPE = list[list[str]]


def load_input(input_path: str = "input.txt") -> PLATFORM_TYPE:
    with open(input_path, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f if line]


def find_place_for_rock_north(
    platform: PLATFORM_TYPE, rock_row: int, rock_col: int
) -> int:
    best_row = rock_row
    for r in range(rock_row - 1, -1, -1):
        if platform[r][rock_col] == ".":
            best_row = r
        else:
            break

    return best_row


def find_place_for_rock_west(
    platform: PLATFORM_TYPE, rock_row: int, rock_col: int
) -> int:
    best_col = rock_col
    for c in range(rock_col - 1, -1, -1):
        if platform[rock_row][c] == ".":
            best_col = c
        else:
            break

    return best_col


def find_place_for_rock_east(
    platform: PLATFORM_TYPE, rock_row: int, rock_col: int
) -> int:
    best_col = rock_col
    for c in range(rock_col + 1, len(platform[rock_row])):
        if platform[rock_row][c] == ".":
            best_col = c
        else:
            break

    return best_col


def find_place_for_rock_south(
    platform: PLATFORM_TYPE, rock_row: int, rock_col: int
) -> int:
    best_row = rock_row
    for r in range(rock_row + 1, len(platform)):
        if platform[r][rock_col] == ".":
            best_row = r
        else:
            break

    return best_row


def tilt_north(platform: PLATFORM_TYPE) -> PLATFORM_TYPE:
    for r, row in enumerate(platform):
        for c, cell in enumerate(row):
            if cell == "O":
                new_row = find_place_for_rock_north(platform, r, c)
                platform[r][c] = "."
                platform[new_row][c] = "O"


def tilt_south(platform: PLATFORM_TYPE) -> PLATFORM_TYPE:
    for r in range(len(platform) - 1, -1, -1):
        row = platform[r]
        for c, cell in enumerate(row):
            if cell == "O":
                new_row = find_place_for_rock_south(platform, r, c)
                platform[r][c] = "."
                platform[new_row][c] = "O"


def tilt_west(platform: PLATFORM_TYPE) -> PLATFORM_TYPE:
    for r, row in enumerate(platform):
        for c, cell in enumerate(row):
            if cell == "O":
                new_col = find_place_for_rock_west(platform, r, c)
                platform[r][c] = "."
                platform[r][new_col] = "O"


def tilt_east(platform: PLATFORM_TYPE) -> PLATFORM_TYPE:
    for r, row in enumerate(platform):
        for c in range(len(row) - 1, -1, -1):
            cell = platform[r][c]
            if cell == "O":
                new_col = find_place_for_rock_east(platform, r, c)
                platform[r][c] = "."
                platform[r][new_col] = "O"


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
    n = 1000000000
    platform = load_input()
    # will store the last time we got the exact same platform
    # used to detect loops
    lasts = {}
    # used to find the load score of each iteration
    loads = []

    for i in range(n):
        tilt_north(platform)
        tilt_west(platform)
        tilt_south(platform)
        tilt_east(platform)

        # hash is used to make the dict use less memory
        h = hash("".join("".join(row) for row in platform))

        # check if we have already encountered the exact same platform
        if h in lasts:
            loop_size = i - lasts[h]  # find when the loop size
            # compute when we got the equivalent state of platform that we will have at n
            end_loop_index = lasts[h] + ((n - lasts[h]) % loop_size) - 1
            final_load = loads[end_loop_index]  # get the load that we will have at n
            break

        lasts[h] = i
        loads.append(compute_load(platform))

    print(final_load)


if __name__ == "__main__":
    main()
