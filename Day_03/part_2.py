from typing import Optional

INPUT_FILE = "input.txt"

ASCII_DIGITS = "0123456789"


def get_number_gear_ratio(
    engine: list[str], row: int, col_start: int, col_end: int
) -> tuple[bool, int]:
    # return 0 if there is no gear ratio
    gear_ratio = 0
    first_number = "".join(engine[row])[col_start : col_end + 1]
    first_number = int(first_number)

    star_position = find_adjacent_star_symbol(engine, row, col_start, col_end)

    if not star_position:
        return False

    # remove the first number
    for i in range(col_start, col_end + 1):
        engine[row][i] = "."

    second_number = find_adjacent_number(engine, star_position[0], star_position[1])

    if second_number:
        gear_ratio = first_number * second_number

    return gear_ratio


def find_adjacent_star_symbol(
    engine: list[str], row: int, col_start: int, col_end: int
) -> tuple[bool, tuple[int, int]]:
    for row_check in range(row - 1, row + 2):
        if row_check < 0 or row_check >= len(engine):
            continue

        line_to_check = engine[row_check]
        for col_check in range(col_start - 1, col_end + 2):
            if col_check < 0 or col_check >= len(line_to_check):
                continue

            if engine[row_check][col_check] == "*":
                # found a star
                return (row_check, col_check)

    return None


def find_nearest_digit(engine: list[list[str]], row: int, col: int) -> tuple[int, int]:
    for row_check in range(row - 1, row + 2):
        if row_check < 0 or row_check >= len(engine):
            continue

        line_to_check = engine[row_check]
        for col_check in range(col - 1, col + 2):
            if col_check < 0 or col_check >= len(line_to_check):
                continue

            if engine[row_check][col_check] in ASCII_DIGITS:
                # found a new digit
                return row_check, col_check

    return None


def find_adjacent_number(engine: list[list[str]], row: int, col: int) -> Optional[int]:
    nearest_digit_position = find_nearest_digit(engine, row, col)
    if not nearest_digit_position:
        return None

    digit_row, digit_col = nearest_digit_position
    found_number_col_start, found_number_col_end = digit_col, digit_col

    # find the start of the number
    for i in range(digit_col, -1, -1):
        if engine[digit_row][i] in ASCII_DIGITS:
            found_number_col_start = i
        else:
            break

    # find the end of the number
    for i in range(digit_col, len(engine[digit_row])):
        if engine[digit_row][i] in ASCII_DIGITS:
            found_number_col_end = i
        else:
            break

    number = "".join(
        engine[digit_row][found_number_col_start : found_number_col_end + 1]
    )
    return int(number)


def load_input(input_path: str) -> list[list[str]]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f if line]


def main():
    engine_schematic = load_input(INPUT_FILE)
    gear_ratio_sum = 0

    # check each row
    for row, line in enumerate(engine_schematic):
        number_start_index: Optional[int] = None
        number_end_index: Optional[int] = None

        # check each char in a column
        line_len = len(line)
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
                    gear_ratio = get_number_gear_ratio(
                        engine_schematic, row, number_start_index, number_end_index
                    )

                    gear_ratio_sum += gear_ratio

                    number_start_index = None
                    number_end_index = None

        if number_end_index is not None:
            gear_ratio = get_number_gear_ratio(
                engine_schematic, row, number_start_index, number_end_index
            )

            gear_ratio_sum += gear_ratio

    print(gear_ratio_sum)


if __name__ == "__main__":
    main()
