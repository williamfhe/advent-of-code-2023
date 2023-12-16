from typing import Iterator


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def parse_input(input_path: str = "input.txt") -> Iterator[str]:
    for line in load_input(input_path):
        for splited in line.split(","):
            yield splited


def compute_hash(string: str) -> int:
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256

    return value


def main():
    total = 0
    for p in parse_input():
        total += compute_hash(p)
    print(total)


if __name__ == "__main__":
    main()
