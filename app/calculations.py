def expected_move_from_atm_straddle(call_premium: float, put_premium: float) -> float:
    if call_premium < 0 or put_premium < 0:
        raise ValueError("Premiums must be non-negative.")
    return round(call_premium + put_premium, 4)
