from __future__ import annotations

from .black_scholes import black_scholes_greeks


def greeks_summary(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> dict[str, float]:
    """Return a subset of Greeks for display/reporting."""
    g = black_scholes_greeks(spot, strike, rate, vol, maturity)
    return {
        "delta_call": g["call_delta"],
        "delta_put": g["put_delta"],
        "gamma": g["gamma"],
        "vega_per_1pct": g["vega"] / 100.0,
        "theta_call": g["call_theta"],
        "theta_put": g["put_theta"],
        "rho_call": g["call_rho"],
        "rho_put": g["put_rho"],
    }
