#!/usr/bin/env python3

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
GAME_ID_PATTERN = re.compile(r"Game (\d+): ")
MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14


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


def day2():
    games = get_input(2)

    possible_games = which_games_possible(games)

    return sum(possible_games)


def which_games_possible(games: list[str], max_red: int = MAX_RED_CUBES,
                         max_green: int = MAX_GREEN_CUBES, max_blue: int = MAX_BLUE_CUBES):
    for game in games:
        game_id, cubes_str = separate_id_and_game(game)
        if is_game_possible(cubes_str, max_blue, max_green, max_red):
            yield game_id


def is_game_possible(cubes_str, max_blue, max_green, max_red):
    rounds = cubes_str.split(";")
    for r in rounds:
        for color in r.split(","):
            match color.strip().split(" "):
                case [number, "red"]:
                    if int(number) > max_red:
                        return False
                case [number, "green"]:
                    if int(number) > max_green:
                        return False
                case [number, "blue"]:
                    if int(number) > max_blue:
                        return False
    return True


def separate_id_and_game(game: str) -> tuple[int, str]:
    match = GAME_ID_PATTERN.match(game)
    num = match.groups()[0]
    num = int(num)
    cubes = game[match.end():]

    return num, cubes


def game_is_possible(red: int, green: int, blue: int, max_red: int, max_green: int, max_blue: int):
    return red <= max_red & green <= max_green & blue <= max_blue


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
    clize.run(day1, day2)
