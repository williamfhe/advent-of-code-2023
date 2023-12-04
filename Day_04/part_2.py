from collections import defaultdict

INPUT_FILE = "input.txt"


def compute_winning_card_count(card: str) -> int:
    _, card_numbers = card.split(": ")
    winning_numbers, numbers_to_check = card_numbers.split(" | ")

    winning_numbers = {number for number in winning_numbers.split(" ") if number}
    numbers_to_check = [number for number in numbers_to_check.split(" ") if number]

    winning_cards = 0
    for number in numbers_to_check:
        if number in winning_numbers:
            winning_cards += 1
    return winning_cards


def load_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def main():
    scratchcards = load_input(INPUT_FILE)
    card_counts = defaultdict(lambda: 1)
    card_counts[0] = 1
    for card_number, card in enumerate(scratchcards):
        winning_cards = compute_winning_card_count(card)
        for i in range(winning_cards):
            card_counts[card_number + i + 1] += card_counts[card_number]

    print(sum(card_counts.values()))


if __name__ == "__main__":
    main()
