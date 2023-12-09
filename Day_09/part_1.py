from typing import Iterator
from collections import deque


def load_input(input_path: str = "input.txt") -> Iterator[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def parse_input(input_path: str = "input.txt") -> Iterator[list[int]]:
    for line in load_input(input_path):
        if not line:
            continue

        yield list(map(int, line.split(" ")))


def find_next_value(line: list[int]) -> int:
    all_lines = deque()
    steps_differences = []
    while True:
        all_lines.append(line)
        steps_differences = []
        steps_are_all_zeros = True
        for i in range(len(line) - 1):
            first = line[i]
            second = line[i + 1]
            difference = second - first
            if difference != 0:
                steps_are_all_zeros = False
            steps_differences.append(difference)

        if steps_are_all_zeros:
            break

        line = steps_differences

    next_value = steps_differences[-1]
    while all_lines:
        last_line = all_lines.pop()
        next_value = last_line[-1] + next_value

    return next_value


def main():
    sum_of_next_values = 0
    for line in parse_input():
        next_value = find_next_value(line)
        sum_of_next_values += next_value
    print(sum_of_next_values)


if __name__ == "__main__":
    main()
