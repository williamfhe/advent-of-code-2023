from typing import Iterator
import functools


def load_input(input_path: str = "input.txt") -> Iterator[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def parse_line(line: str) -> tuple[str, tuple[int]]:
    springs, numbers = line.split(" ")
    numbers = [int(number) for number in numbers.split(",")]
    return springs, tuple(numbers)


@functools.cache  # for great speedup
def count_all_possible_combinations(
    springs_template: str, conditions: tuple[int], current=""
) -> int:
    if not conditions:
        # there are still springs groups in the template
        if "#" in springs_template:
            return 0

        # we are at the end of a spring
        return 1

    valid_permutations = 0
    for i in range(len(springs_template) - sum(conditions[1:]) - len(conditions) + 1):
        if "#" in springs_template[:i]:
            break

        permut = "." * i + "#" * conditions[0]
        if len(permut) < len(springs_template):
            permut += "."

        if len(permut) > len(springs_template):
            break

        # check if substrings are equals and ignore the "?"
        for s, p in zip(springs_template, permut):
            # check if the spring's char is the one from the permutation or a "?"
            if s not in (p, "?"):
                break
        else:
            # the substrings are equals ("?" ignored)
            valid_permutations += count_all_possible_combinations(
                springs_template[len(permut) :],
                conditions[1:],
            )

    return valid_permutations


def main():
    # running with pypy makes the result really fast
    challenge_input = load_input()

    all_permutations = 0
    for line in challenge_input:
        springs, conditions = parse_line(line)

        # duplicate by 5
        springs = (springs + "?") * 5
        springs = springs[:-1]
        conditions = conditions * 5

        count = count_all_possible_combinations(springs, conditions)
        # print(f"{springs=} {conditions=} {count=}")
        all_permutations += count
    print(all_permutations)


if __name__ == "__main__":
    main()
