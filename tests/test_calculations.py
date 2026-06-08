import pytest

from app.calculations import expected_move_from_atm_straddle


def test_expected_move_from_atm_straddle_adds_premiums() -> None:
    assert expected_move_from_atm_straddle(2.15, 1.85) == 4.0


def test_expected_move_from_atm_straddle_rejects_negative_premiums() -> None:
    with pytest.raises(ValueError):
        expected_move_from_atm_straddle(-0.1, 1.0)
