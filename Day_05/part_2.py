from collections import defaultdict
from typing import Optional

# contains DEST_START, SRC_START, location_range_length
SEED_LOCATION_RANGE_TYPE = tuple[int, int, int]
SEED_RANGE_TYPE = tuple[int, int]
SEED_TYPES = tuple[int]

PARSED_ALMANAC_TYPE = dict[list[SEED_LOCATION_RANGE_TYPE]]


# Used to simplify working with ranges
class AlmanacRange:
    def __init__(self, start: int, length: int):
        self.__start = start
        self.__length = length

    @property
    def start(self) -> int:
        return self.__start

    @property
    def length(self) -> int:
        return self.__length

    @property
    def end(self) -> int:
        return self.__start + self.__length - 1

    def intersect(self, other: "AlmanacRange") -> bool:
        if self.end < other.start:
            return False

        if self.start > other.end:
            return False

        return True

    def transpose_start(self, move_step: int):
        """Used for range destination.

        Args:
            move_step (int): how much to move the start
        """
        self.__start += move_step

    def get_intersection(self, other: "AlmanacRange") -> Optional["AlmanacRange"]:
        """Returns the intersection of two ranges

        Returns:
            AlmanacRange | None: a new AlamanacRange that contains the intersection.
        """
        if not self.intersect(other):
            return None

        intersection_start = max(self.start, other.start)
        intersection_end = min(self.end, other.end)
        intersection_length = intersection_end - intersection_start + 1

        return AlmanacRange(intersection_start, intersection_length)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{{start={self.__start} end={self.end} length={self.__length}}}"


def split_ranges_if_intersect(
    seed: AlmanacRange, location: AlmanacRange
) -> tuple[AlmanacRange | None, AlmanacRange | None, AlmanacRange | None]:
    """Split the seed range in the three if there is an intersection:

    Left part (optional)
    Intersection of seed and location
    Right part (optional)

    Args:
        seed (AlmanacRange): The seed range
        location (AlmanacRange): The range that contain a location for the seed

    Returns:
        AlmanacRange | None: The left part if there is one
        AlmanacRange | None: The intersection of seed & location if there is one
        AlmanacRange | None: The right part if there is one
    """
    intersection = seed.get_intersection(location)

    if not intersection:
        return None, None, None

    left_range, right_range = None, None

    no_range_at_left = intersection.start == seed.start
    if not no_range_at_left:
        left_range_end = max(seed.start, intersection.start)
        left_range_start = min(seed.start, intersection.start)
        left_range_length = left_range_end - left_range_start
        left_range = AlmanacRange(left_range_start, left_range_length)

    no_range_at_right = intersection.end == seed.end
    if not no_range_at_right:
        right_range_start = min(intersection.end, seed.end) + 1
        right_range_end = max(intersection.end, seed.end)
        right_range_length = right_range_end - right_range_start + 1
        right_range = AlmanacRange(right_range_start, right_range_length)

    return left_range, intersection, right_range


def merge_ranges(ranges: list[AlmanacRange]) -> list[AlmanacRange]:
    """Merge ranges that intersects or collide so we have less to work with.

    Example :

    0->15 and 10->20 intersects so we can merge them in 0->20
    0->15 and 16->20 "collides" so we can merge them in 0->20
    0->15 and 20->30 do not collide or intersects so we keep them both

    Args:
        ranges (list[AlmanacRange]): The ranges to check for merges

    Returns:
        list[AlmanacRange]: The merged ranges
    """
    if not ranges:
        return []

    # sort from lowest to greatest
    sorted_ranges = sorted(ranges, key=lambda r: r.start)

    new_ranges = []

    current_range = sorted_ranges[0]

    i = 1
    while i < len(sorted_ranges):
        range_to_check = sorted_ranges[i]
        i += 1

        if (
            not current_range.intersect(range_to_check)
            and not current_range.end + 1 == range_to_check.start
        ):
            new_ranges.append(current_range)
            current_range = range_to_check
            continue

        new_range_start = min(current_range.start, range_to_check.start)
        new_range_end = max(current_range.end, range_to_check.end)
        new_range_length = new_range_end - new_range_start + 1
        current_range = AlmanacRange(new_range_start, new_range_length)

    new_ranges.append(current_range)

    return new_ranges


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


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

    # create instances of Almanac using each seed pair
    seed_ranges = [
        AlmanacRange(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]

    i = 0
    for category_name, category_ranges in parsed_almanac.items():
        # print(f"Checking {category_name=} {len(category_ranges)=}")
        i += 1
        next_category_ranges = []
        next_seedloop_ranges = []

        # check each category ranges
        for dest, start, length in category_ranges:
            location_range = AlmanacRange(start, length)

            # next_seedloop_ranges are the seed ranges that we check for the
            # next location of the current category. If there is an intersection
            # between a seed range and a location, its value is updated to include
            # the left and right parts of the intersection.
            next_seedloop_ranges = []

            # should_retry indicates if we need to check again the seeds
            # this code should probably have been refactored
            should_retry = True
            while should_retry:
                should_retry = False
                for seed_range in seed_ranges:
                    left_range, intersection, right_range = split_ranges_if_intersect(
                        seed_range, location_range
                    )
                    if not intersection:
                        # no intersection betweens the seeds and the location
                        next_seedloop_ranges.append(seed_range)
                        continue

                    # move the range that is the intersection to its destionation
                    intersection.transpose_start(dest - start)

                    # the intersection should not be reused until we browse the next category
                    next_category_ranges.append(intersection)

                    if left_range:
                        # reuse the left part for the next location in the current category
                        next_seedloop_ranges.append(left_range)
                        # there are other seed ranges to check
                        should_retry = True

                    if right_range:
                        # reuse the right part for the next location in the current category
                        next_seedloop_ranges.append(right_range)
                        # there are other seed ranges to check
                        should_retry = True

                # merging ranges is optional but allows us to have less ranges to work with
                seed_ranges = merge_ranges(next_seedloop_ranges)

        # merging ranges is optional but allows us to have less ranges to work with
        seed_ranges = merge_ranges(next_category_ranges + next_seedloop_ranges)

    seed_ranges = merge_ranges(seed_ranges)

    # the lowest seed is lowest start of a range
    lowest_seed = sorted(seed_ranges, key=lambda r: r.start)[0].start

    print(lowest_seed)


if __name__ == "__main__":
    main()
