from enum import IntEnum
from collections import Counter
from functools import cmp_to_key


class HandType(IntEnum):
    HighCard = 0
    OnePair = 1
    TwoPair = 2
    ThreeOfAKind = 3
    FullHouse = 4
    FourOfAKind = 5
    FiveOfAKind = 6


POSSIBLE_CARDS = {c: i for i, c in enumerate("J23456789TQKA")}


def get_hand_type(hand: str) -> HandType:
    card_count = Counter(hand)
    hand_type = None
    if "J" in hand and hand != "JJJJJ":
        j_count = card_count.pop("J")
        card_counted_the_most = card_count.most_common(1)[0][0]
        card_count[card_counted_the_most] += j_count

    match len(card_count):
        case 5:
            hand_type = HandType.HighCard
        case 4:
            hand_type = HandType.OnePair
        case 3:
            # two pair / three of a kind
            if sorted(card_count.values()) == [1, 2, 2]:
                hand_type = HandType.TwoPair
            else:
                hand_type = HandType.ThreeOfAKind

        case 2:
            # full house / foud of a kind
            if sorted(card_count.values()) == [2, 3]:
                hand_type = HandType.FullHouse
            else:
                hand_type = HandType.FourOfAKind

        case 1:
            return HandType.FiveOfAKind

    return hand_type


def compare_hands(first_hand: str, second_hand: str) -> int:
    first_hand_type = get_hand_type(first_hand)
    second_hand_type = get_hand_type(second_hand)

    if first_hand_type > second_hand_type:
        return 1

    if first_hand_type < second_hand_type:
        return -1

    # both hands are equals, now we need to sort

    for c1, c2 in zip(first_hand, second_hand):
        c1_char_index = POSSIBLE_CARDS[c1]
        c2_char_index = POSSIBLE_CARDS[c2]
        if c1_char_index > c2_char_index:
            return 1

        if c1_char_index < c2_char_index:
            return -1

    return 0


def load_input(input_path: str = "input.txt") -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def parse_input(input_path: str = "input.txt") -> list[tuple[str, int]]:
    for line in load_input(input_path):
        if not line:
            continue

        hand = line[:5]
        bid_str = line[6:]
        yield hand, int(bid_str)


def main():
    total_winnings = 0
    hand_to_bid = {hand: bid for hand, bid in parse_input()}

    sorted_hands = sorted(hand_to_bid.keys(), key=cmp_to_key(compare_hands))
    for rank, hand in enumerate(sorted_hands):
        total_winnings += hand_to_bid[hand] * (rank + 1)

    print(total_winnings)


if __name__ == "__main__":
    main()
