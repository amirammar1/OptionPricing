from __future__ import annotations

import math

from scipy.stats import norm

# --- Core formulas ---


def _d1(spot: float, strike: float, rate: float, vol: float, maturity: float) -> float:
    num = math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity
    den = vol * math.sqrt(maturity)
    return num / den


def _d2(d1: float, vol: float, maturity: float) -> float:
    return d1 - vol * math.sqrt(maturity)

def black_scholes_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    option_type: str,
) -> float:
    """Closed-form Black–Scholes price for European call/put.

    Args:
        spot: Current underlying spot price S0.
        strike: Strike price K.
        rate: Risk-free continuously compounded rate r.
        vol: Volatility sigma.
        maturity: Time to maturity T in years.
        option_type: 'call' or 'put'.
    """
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")
    if maturity <= 0 or vol <= 0 or strike <= 0 or spot <= 0:
        raise ValueError("Inputs must be positive and maturity>0")

    d1 = _d1(spot, strike, rate, vol, maturity)
    d2 = _d2(d1, vol, maturity)
    df = math.exp(-rate * maturity)

    if option_type == "call":
        return spot * norm.cdf(d1) - strike * df * norm.cdf(d2)
    else:
        return strike * df * norm.cdf(-d2) - spot * norm.cdf(-d1)


def black_scholes_greeks(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> dict[str, float]:
    """Return primary Greeks for a European call option (signs adapted for puts separately)."""
    d1 = _d1(spot, strike, rate, vol, maturity)
    d2 = _d2(d1, vol, maturity)
    df = math.exp(-rate * maturity)
    nd1 = norm.pdf(d1)

    call_delta = norm.cdf(d1)
    put_delta = call_delta - 1.0
    gamma = nd1 / (spot * vol * math.sqrt(maturity))
    vega = spot * nd1 * math.sqrt(maturity)  # per 1.0 vol (not 1%)
    call_theta = (
        -(spot * nd1 * vol) / (2 * math.sqrt(maturity))
        - rate * strike * df * norm.cdf(d2)
    )
    put_theta = (
        -(spot * nd1 * vol) / (2 * math.sqrt(maturity))
        + rate * strike * df * norm.cdf(-d2)
    )
    call_rho = maturity * strike * df * norm.cdf(d2)
    put_rho = -maturity * strike * df * norm.cdf(-d2)

    return {
        "call_delta": call_delta,
        "put_delta": put_delta,
        "gamma": gamma,
        "vega": vega,
        "call_theta": call_theta,
        "put_theta": put_theta,
        "call_rho": call_rho,
        "put_rho": put_rho,
    }


def call_put_parity(
    call_price: float,
    spot: float,
    strike: float,
    rate: float,
    maturity: float,
) -> float:
    """Return implied put price from call using put-call parity."""
    return call_price - spot + strike * math.exp(-rate * maturity)


def implied_volatility(
    price: float,
    spot: float,
    strike: float,
    rate: float,
    maturity: float,
    option_type: str,
    *,
    tol: float = 1e-8,
    max_iter: int = 100,
) -> float:
    """Compute Black–Scholes implied volatility via Newton–Raphson."""
    if price <= 0:
        raise ValueError("Price must be positive")
    vol = 0.2  # initial guess
    for _ in range(max_iter):
        bs_price = black_scholes_price(spot, strike, rate, vol, maturity, option_type)
        diff = bs_price - price
        if abs(diff) < tol:
            return vol
        greeks = black_scholes_greeks(spot, strike, rate, vol, maturity)
        vega = greeks["vega"]
        if vega < 1e-12:
            break
        vol -= diff / vega
        if vol <= 0:
            vol = 1e-4
    raise RuntimeError("Implied volatility did not converge")
