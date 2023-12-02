from typing import Optional

INPUT_FILE = "input.txt"

ASCII_DIGITS = "0123456789"

NAME_TO_DIGIT_CHAR = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


calibration_sum = 0
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        first_digit: Optional[str] = None
        last_digit: Optional[str] = None
        line_len = len(line)

        # iterate over each char using the index
        for i in range(line_len):
            found_digit: Optional[str] = None
            char = line[i]

            # check if the current char is a digit
            if char in ASCII_DIGITS:
                found_digit = char
            else:
                # check if the current char is the start of a digit name
                for digit_name, digit_char in NAME_TO_DIGIT_CHAR.items():
                    digit_name_len = len(digit_name)
                    if i + digit_name_len > len(line):
                        # the remaining line is too short to be a digit name
                        continue

                    # check if the substring is the digit name
                    if line[i : i + digit_name_len] == digit_name:
                        found_digit = digit_char
                        break

            # check if we found a digit
            if found_digit:
                # find is the digit is the first or last of the line
                if first_digit is None:
                    first_digit = found_digit
                else:
                    last_digit = found_digit

        # calibration definition
        if first_digit is None:
            continue

        if last_digit is None:
            calibration = first_digit + first_digit
        else:
            calibration = first_digit + last_digit

        print(calibration)
        calibration = int(calibration)
        calibration_sum += calibration

print(calibration_sum)
