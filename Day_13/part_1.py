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


def find_possible_mirrors_in_line(pattern_line: str) -> set[int]:
    possible_mirrors = set()
    for i in range(len(pattern_line) // 2, 0, -1):
        j = i
        j2 = j * 2
        zone = pattern_line[:j]
        mirror = "".join(reversed(pattern_line[j:j2]))

        if zone == mirror:
            possible_mirrors.add(len(zone))

        # if the mirror has an odd size we need to also check from the end
        # exemple pattern = 12345
        # left : 1/2 12/34 - right : 23/45 4/5
        if len(pattern_line) % 2 != 0:
            zone = pattern_line[-j:]
            mirror = "".join(reversed(pattern_line[-j2:-j]))
            if zone == mirror:
                possible_mirrors.add(len(pattern_line) - len(zone))

    return possible_mirrors


def find_mirror(patterns: list[str]) -> Optional[int]:
    possible_mirrors = find_possible_mirrors_in_line(patterns[0])

    for row in patterns[1:]:
        line_mirrors = find_possible_mirrors_in_line(row)
        possible_mirrors = possible_mirrors.intersection(line_mirrors)
        if not possible_mirrors:
            return None

    if possible_mirrors:
        if len(possible_mirrors) != 1:
            raise ValueError("Multiple possible mirrors")
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
    if vertical_mirror := find_mirror(patterns):
        return vertical_mirror

    rotated_pattern = rotate_patterns(patterns)

    if horizontal_mirror := find_mirror(rotated_pattern):
        return 100 * horizontal_mirror

    raise ValueError("No mirror found")


def main():
    total_score = 0
    for pattern in parse_input():
        total_score += compute_mirror_score(pattern)
    print(total_score)


if __name__ == "__main__":
    main()
