def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def main():
    challenge_input = load_input()
    for line in challenge_input:
        print(line)


if __name__ == "__main__":
    main()
