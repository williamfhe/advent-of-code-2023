from collections import defaultdict

# contains DEST_START, SRC_START, RANGE_LENGTH
SEED_RANGE_TYPE = tuple[int, int, int]
SEED_TYPES = tuple[int]

PARSED_ALMANAC_TYPE = dict[list[SEED_RANGE_TYPE]]


def convert_seeds(seed: int, seed_ranges: list[SEED_RANGE_TYPE]) -> int:
    for seed_range in seed_ranges:
        destination_range_start, source_range_start, range_length = seed_range

        if source_range_start <= seed <= source_range_start + range_length - 1:
            return seed - source_range_start + destination_range_start

    return seed


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def print_all_converted_seed(seed_ranges: list[SEED_RANGE_TYPE]):
    for seed in range(101):
        new_location = convert_seeds(seed, seed_ranges)
        # new_location = seed_converter(seed, 50, 98, 2)
        print(f"{seed=} {new_location=}")


def parse_input_integer_line(line: str) -> tuple[int]:
    return tuple(map(int, [value for value in line.split(" ")]))


def parse_almanac(almanac: list[str]) -> tuple[SEED_TYPES, PARSED_ALMANAC_TYPE]:
    # read the seeds (first line)
    seeds = parse_input_integer_line(almanac[0][7:])

    # will contains all category / ranges
    almanac_content = defaultdict(list)

    category_name = ""
    for line in almanac[1:]:
        if not line:
            # ignore empty lines
            continue

        if line.endswith("map:"):
            category_name = line[:-5]
            continue

        range_values = parse_input_integer_line(line)
        almanac_content[category_name].append(range_values)

    return seeds, almanac_content


def main():
    raw_alamanac = load_input()
    seeds, parsed_almanac = parse_almanac(raw_alamanac)
    lowest_location = None
    for seed in seeds:
        for seed_ranges in parsed_almanac.values():
            new_seed_value = convert_seeds(seed, seed_ranges)
            seed = new_seed_value

        if lowest_location is None or seed < lowest_location:
            lowest_location = seed

    print(lowest_location)


if __name__ == "__main__":
    main()
