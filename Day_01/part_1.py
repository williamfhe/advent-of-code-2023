from typing import Optional

INPUT_FILE = "input.txt"

ASCII_DIGITS = "0123456789"

calibration_sum = 0
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        first_digit: Optional[str] = None
        last_digit: Optional[str] = None
        for char in line:
            if char in ASCII_DIGITS:
                if first_digit is None:
                    first_digit = char
                else:
                    last_digit = char

        if first_digit is None:
            continue

        if last_digit is None:
            calibration = first_digit + first_digit
        else:
            calibration = first_digit + last_digit

        calibration = int(calibration)
        calibration_sum += calibration

print(calibration_sum)
