from typing import Iterator, Optional


def load_input(input_path: str = "input.txt") -> Iterator[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def parse_input(input_path: str = "input.txt") -> Iterator[list[str]]:
    current_map = []
    for line in load_input(input_path):
        if line:
            current_map.append(line)
        else:
            if current_map:
                yield current_map
            current_map = []

    if current_map:
        yield current_map


def count_differences(first: str, second: str) -> int:
    if len(first) != len(second):
        raise ValueError("Both strings aren't of the same size")
    diffences = 0
    for f, s in zip(first, second):
        if f != s:
            diffences += 1
    return diffences


def find_possible_mirrors_in_line(
    pattern_line: str, found_smudges: set[int]
) -> set[int]:
    possible_mirrors = set()

    for i in range(len(pattern_line) // 2, 0, -1):
        j = i
        j2 = j * 2
        zone = pattern_line[:j]
        left_of_mirror = len(zone)
        mirror = "".join(reversed(pattern_line[j:j2]))

        diff = count_differences(zone, mirror)
        if diff == 0:  # zone and reflection (mirror) are the same
            possible_mirrors.add(left_of_mirror)
        elif diff == 1 and left_of_mirror not in found_smudges:
            # we found the smudge in the mirror
            found_smudges.add(left_of_mirror)
            possible_mirrors.add(left_of_mirror)

        # if the mirror has an odd size we need to also check from the end
        # exemple pattern = 12345
        # left : 1/2 12/34 - right : 23/45 4/5
        if len(pattern_line) % 2 != 0:
            zone = pattern_line[-j:]
            mirror = "".join(reversed(pattern_line[-j2:-j]))
            left_of_mirror = len(pattern_line) - len(zone)

            diff = count_differences(zone, mirror)
            if diff == 0:  # zone and reflection (mirror) are the same
                possible_mirrors.add(left_of_mirror)
            elif diff == 1 and left_of_mirror not in found_smudges:
                # we found the smudge in the mirror
                found_smudges.add(left_of_mirror)
                possible_mirrors.add(left_of_mirror)

    return possible_mirrors, found_smudges


def find_mirror(patterns: list[str]) -> Optional[int]:
    possible_mirrors, found_smudges = find_possible_mirrors_in_line(patterns[0], set())

    for row in patterns[1:]:
        line_mirrors, found_smudges = find_possible_mirrors_in_line(row, found_smudges)
        possible_mirrors = possible_mirrors.intersection(line_mirrors)
        if not possible_mirrors:
            return None

    # our mirror must have a smudge
    possible_mirrors = possible_mirrors.intersection(found_smudges)
    if possible_mirrors:
        if len(possible_mirrors) != 1:
            raise ValueError(
                f"found multiple possible mirrors {possible_mirrors=} {found_smudges=}"
            )
        return possible_mirrors.pop()
    return None


def rotate_patterns(patterns: list[str]) -> list[str]:
    returned_patterns = []
    for col in range(len(patterns[0])):
        line = ""
        for row in range(len(patterns)):
            line += patterns[row][col]

        returned_patterns.append(line)
    return returned_patterns


def compute_mirror_score(patterns: list[str]) -> int:
    rotated_pattern = rotate_patterns(patterns)
    if horizontal_mirror := find_mirror(rotated_pattern):
        return 100 * horizontal_mirror

    if vertical_mirror := find_mirror(patterns):
        return vertical_mirror

    raise ValueError("No mirror found")


def main():
    total_score = 0
    for pattern in parse_input():
        total_score += compute_mirror_score(pattern)
    print(total_score)


if __name__ == "__main__":
    main()
