from pathlib import Path

from solutions import sum_all_calibrations, extract_calibration, which_games_possible

TEST_ROOT = Path(__file__).parent


def get_input(n: str):
    with (TEST_ROOT / "input" / f"{n}").open("r") as f:
        return f.readlines()


def test_decode_calibration_digits():
    input_ = get_input("1.txt")

    result = sum_all_calibrations(input_)

    assert result == 142


def test_decode_calibration_written_digits():
    input_ = get_input("1_2.txt")
    summed = sum_all_calibrations(input_)

    assert summed == 281


def test_decode_one_written_number_counts_double():
    calibration = extract_calibration("one")

    assert calibration == 11


def test_decode_overlapping_words():
    calibration = extract_calibration("twone")
    assert calibration == 21


def test_possible_games():
    input_ = get_input("2.txt")

    possible_games = which_games_possible(input_)

    assert list(possible_games) == [1, 2, 5]
