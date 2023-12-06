def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def parse_input(challenge_input: list[str]) -> dict[int, int]:
    time_str, distance_str = challenge_input
    times = map(int, [value for value in time_str[10:].split(" ") if value])
    distances = map(int, [value for value in distance_str[10:].split(" ") if value])
    return {time: dist for time, dist in zip(times, distances)}


def count_wins(time: int, distance_to_beat: int) -> int:
    wins = 0
    for i in range(0, time + 1):
        speed = i
        duration = time - i
        dist = speed * duration
        if dist > distance_to_beat:
            wins += 1
    return wins


def main():
    challenge_input = load_input()
    course_times = parse_input(challenge_input)
    number_of_wins = 1
    for time, distance in course_times.items():
        number_of_wins *= count_wins(time, distance)

    print(number_of_wins)


if __name__ == "__main__":
    main()
