import re
import logging
import clize
from pathlib import Path
import os

log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)
_logger = logging.getLogger()

NUMBER_PATTERN = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"
NUMBER_PATTERN = re.compile(NUMBER_PATTERN)
TEXT_NUMBER_MAP = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def text_to_number(text: str) -> int:
    index = TEXT_NUMBER_MAP.index(text)
    return index + 1


def get_input(day):
    filepath = Path(f"input/{day}.txt")
    with filepath.open("r") as f:
        return f.readlines()


def day1():
    input_ = get_input(1)
    summed = sum_all_calibrations(input_)

    return summed


def extract_calibration(line: str) -> int:
    matches = NUMBER_PATTERN.finditer(line)
    numbers = [m.group(1) for m in matches]

    calibration_nums = numbers[0], numbers[-1]
    calibration_nums = [convert_calibration_num(num) for num in calibration_nums]
    joined = "".join(calibration_nums)
    result = int(joined)

    return result


def convert_calibration_num(num: str):
    if re.match(r"\d", num):
        return num
    else:
        return str(text_to_number(num))


def sum_all_calibrations(input_: list[str]) -> int:
    summed = 0
    for idx, line in enumerate(input_):
        extracted = extract_calibration(line)
        summed += extracted

        _logger.debug(f"{idx}: from {line} to {extracted}")
    return summed


if __name__ == "__main__":
    clize.run(day1)
