from pathlib import Path
from solutions import extract_all_calibrations

TEST_ROOT = Path(__file__).parent


def get_input(n: int):
    with (TEST_ROOT / "input" / f"{n}.txt").open("r") as f:
        return f.readlines()


def test_decode_calibration():
    input_ = get_input(1)

    calibrations = extract_all_calibrations(input_)

    assert calibrations == [12, 38, 15, 77]
