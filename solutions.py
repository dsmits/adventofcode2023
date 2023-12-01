import clize
from pathlib import Path


def get_input(day):
    filepath = Path(f"input/{day}.txt")
    with filepath.open("r") as f:
        return f.readlines()


def day1():
    input_ = get_input(1)
    calibrations = extract_all_calibrations(input_)

    return sum(calibrations)


def extract_calibration(line: str) -> int:
    calibration = ""
    for char in line:
        if char in "0123456789":
            calibration += char

    return int(calibration[0] + calibration[-1])


def extract_all_calibrations(input_: list[str]):
    return [extract_calibration(line) for line in input_]


if __name__ == "__main__":
    clize.run(day1)
