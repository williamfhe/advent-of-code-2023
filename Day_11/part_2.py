def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def get_galaxies_positions(space_map: list[str]) -> list[tuple[int, int]]:
    w = len(space_map[0])
    h = len(space_map)
    empty_rows = set(range(h))
    empty_columns = set(range(w))

    for r in range(h):
        for c in range(w):
            if space_map[r][c] == "#":
                empty_rows.discard(r)
                empty_columns.discard(c)

    offset_size = 1000000 - 1
    galaxies = []
    offset_row = 0
    for r in range(h):
        if r in empty_rows:
            offset_row += offset_size
            continue
        offset_columns = 0
        for c in range(w):
            if c in empty_columns:
                offset_columns += offset_size
                continue

            if space_map[r][c] == "#":
                galaxies.append((r + offset_row, c + offset_columns))

    return galaxies


def compute_galaxies_distances(galaxies: list[tuple[int, int]]) -> int:
    sum_of_all_distances = 0
    for i in range(len(galaxies)):
        for j in range(i, len(galaxies)):
            distance = abs(galaxies[j][0] - galaxies[i][0]) + abs(
                galaxies[j][1] - galaxies[i][1]
            )
            sum_of_all_distances += distance
    return sum_of_all_distances


def main():
    space_map = load_input()

    galaxies = get_galaxies_positions(space_map)
    sum_of_all_distances = compute_galaxies_distances(galaxies)
    print(sum_of_all_distances)


if __name__ == "__main__":
    main()
