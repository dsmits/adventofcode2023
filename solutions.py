#!/usr/bin/env python3

import re
import logging
from collections import namedtuple

import clize
from pathlib import Path
import os

log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)
_logger = logging.getLogger()

# Day 1
NUMBER_PATTERN = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"
NUMBER_PATTERN = re.compile(NUMBER_PATTERN)
TEXT_NUMBER_MAP = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

# Day 2
GAME_ID_PATTERN = re.compile(r"Game (\d+): ")
MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14
CubeRound = namedtuple("CubeRound", ["red", "green", "blue"])

# Day 3
SYMBOL_PATTERN = re.compile(r"[^\d|.|\n]")
PART_NUMBER_PATTERN = re.compile(r"\d+")


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


def day2():
    games = get_input(2)

    possible_games = which_games_possible(games)
    powers = compute_cube_powers(games)

    return sum(possible_games), sum(powers)


def which_games_possible(games: list[str], max_red: int = MAX_RED_CUBES,
                         max_green: int = MAX_GREEN_CUBES, max_blue: int = MAX_BLUE_CUBES):
    for game in games:
        game_id, parsed_rounds = parse_game(game)
        if is_game_possible(parsed_rounds, max_blue, max_green, max_red):
            yield game_id


def compute_cube_powers(games):
    # If there is no color in a round, the max will be 1. This way it doesn't affect the
    # multiplication

    for game in games:
        max_red = max_green = max_blue = 1
        game_id, rounds = parse_game(game)
        for round_ in rounds:
            if round_.red > max_red:
                max_red = round_.red
            if round_.green > max_green:
                max_green = round_.green
            if round_.blue > max_blue:
                max_blue = round_.blue

        power = max_red * max_green * max_blue
        yield power


def is_game_possible(parsed_rounds: list[CubeRound], max_blue, max_green, max_red):
    for r in parsed_rounds:
        if r.red > max_red:
            return False
        if r.green > max_green:
            return False
        if r.blue > max_blue:
            return False
    return True


def parse_game(game: str) -> tuple[int, list[CubeRound]]:
    match = GAME_ID_PATTERN.match(game)
    num = match.groups()[0]
    num = int(num)
    cubes = game[match.end():]

    rounds = cubes.split(";")
    parsed_rounds = []
    for r in rounds:
        red = green = blue = 0

        for color in r.split(","):
            match color.strip().split(" "):
                case [number, "red"]:
                    red = int(number)
                case [number, "green"]:
                    green = int(number)
                case [number, "blue"]:
                    blue = int(number)

        parsed_rounds.append(CubeRound(red, green, blue))
    return num, parsed_rounds


def game_is_possible(red: int, green: int, blue: int, max_red: int, max_green: int,
                     max_blue: int):
    return red <= max_red & green <= max_green & blue <= max_blue


def day3():
    input_ = get_input(3)

    return sum_part_numbers(input_)


def sum_part_numbers(lines):
    return sum(get_part_numbers(lines))


def get_part_numbers(lines):
    for idx, line in enumerate(lines):
        for match in PART_NUMBER_PATTERN.finditer(line):
            span = match.span()
            column_limits = max(span[0] - 1, 0), min(span[1] + 1, len(line) - 1)

            column_coords = range(*column_limits)
            row_coords = [idx]

            if idx > 1:
                row_coords.append(idx - 1)
            if idx < len(lines) - 1:
                row_coords.append(idx + 1)

            if contains_symbol(row_coords, column_coords, lines):
                yield int(match.group())


def contains_symbol(row_coords, column_coords, lines):
    for col in column_coords:
        for row in row_coords:
            if SYMBOL_PATTERN.match(lines[row][col]):
                return True

    return False


def is_symbol(char: str) -> bool:
    return re.match(r"\d|.", char) is None


def extract_full_number(idx, line):
    previous = idx
    start = idx
    end = idx
    # Find front
    for i in range(idx, 0):
        if not line[i].isdigit():
            start = previous
            break
        previous = i

    # Find end
    previous = idx
    for i in range(idx, len(line)):
        if not line[i].isdigit():
            end = previous
            break
        previous = i

    return int(line[start:end + 1])


if __name__ == "__main__":
    clize.run(day1, day2, day3)
