from option_pricing.black_scholes import black_scholes_price, implied_volatility


def test_call_put_parity():
    c = black_scholes_price(100, 100, 0.01, 0.2, 1.0, "call")
    p = black_scholes_price(100, 100, 0.01, 0.2, 1.0, "put")
    # Put-call parity: C - P = S - K e^{-rT}
    from math import exp
    lhs = c - p
    rhs = 100 - 100 * exp(-0.01 * 1.0)
    assert abs(lhs - rhs) < 1e-8


def test_implied_volatility_recovers():
    price = black_scholes_price(100, 110, 0.01, 0.35, 2.0, "call")
    iv = implied_volatility(price, 100, 110, 0.01, 2.0, "call")
    assert abs(iv - 0.35) < 1e-4
