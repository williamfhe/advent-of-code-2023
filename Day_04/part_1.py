INPUT_FILE = "input.txt"


def compute_card_points(card: str) -> int:
    _, card_numbers = card.split(": ")
    winning_numbers, numbers_to_check = card_numbers.split(" | ")

    winning_numbers = {number for number in winning_numbers.split(" ") if number}
    numbers_to_check = [number for number in numbers_to_check.split(" ") if number]

    card_points = 0
    for number in numbers_to_check:
        if number in winning_numbers:
            if card_points == 0:
                card_points = 1
            else:
                card_points *= 2

    return card_points


def load_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def main():
    total_points = 0
    scratchcards = load_input(INPUT_FILE)
    for card in scratchcards:
        card_points = compute_card_points(card)
        total_points += card_points

    print(total_points)


if __name__ == "__main__":
    main()
