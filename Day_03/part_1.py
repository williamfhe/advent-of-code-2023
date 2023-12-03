from typing import Optional

INPUT_FILE = "input.txt"

ASCII_DIGITS = "0123456789"


def check_if_number_is_valid(
    engine: list[str], row: int, col_start: int, col_end: int
) -> tuple[bool, int]:
    number = int(engine[row][col_start : col_end + 1])

    is_adjacent = is_number_adjacent_to_symbol(engine, row, col_start, col_end)

    return is_adjacent, number


def is_number_adjacent_to_symbol(
    engine: list[str], row: int, col_start: int, col_end: int
) -> bool:
    for row_check in range(row - 1, row + 2):
        if row_check < 0 or row_check >= len(engine):
            continue

        line_to_check = engine[row_check]
        for col_check in range(col_start - 1, col_end + 2):
            if col_check < 0 or col_check >= len(line_to_check):
                continue

            if (
                engine[row_check][col_check] != "."
                and engine[row_check][col_check] not in ASCII_DIGITS
            ):
                return True

    return False


def load_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line]


def main():
    engine_schematic = load_input(INPUT_FILE)
    number_sum = 0

    # check each row
    for row, line in enumerate(engine_schematic):
        number_start_index: Optional[int] = None
        number_end_index: Optional[int] = None

        # check each char in a column
        for col, char in enumerate(line):
            # check if the current char is a digit
            if char in ASCII_DIGITS:
                if number_start_index is None:
                    number_start_index = col
                    number_end_index = col
                else:
                    number_end_index = col
            else:
                # the char is not a digit

                # check if the number has just ended
                if number_end_index is not None:
                    is_valid, number = check_if_number_is_valid(
                        engine_schematic, row, number_start_index, number_end_index
                    )

                    if is_valid:
                        number_sum += number

                    number_start_index = None
                    number_end_index = None

        if number_end_index is not None:
            is_valid, number = check_if_number_is_valid(
                engine_schematic, row, number_start_index, number_end_index
            )

            if is_valid:
                number_sum += number

    print(number_sum)


if __name__ == "__main__":
    main()
