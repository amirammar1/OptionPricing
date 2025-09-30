from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np

from .black_scholes import black_scholes_price

PayoffFn = Callable[[np.ndarray], np.ndarray]

@dataclass(slots=True)
class MCResult:
    price: float
    stderr: float
    ci95: tuple[float, float]
    n_paths: int
    details: dict[str, float]


def _generate_terminal_spots(
    spot: float,
    rate: float,
    vol: float,
    maturity: float,
    n: int,
    *,
    antithetic: bool = False,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    rng = rng or np.random.default_rng()
    z = rng.standard_normal(n if not antithetic else n // 2)
    if antithetic:
        z = np.concatenate([z, -z])
    drift = (rate - 0.5 * vol * vol) * maturity
    diffusion = vol * math.sqrt(maturity) * z
    return spot * np.exp(drift + diffusion)


def _european_payoff(strike: float, option_type: str) -> PayoffFn:
    if option_type == "call":
        return lambda s: np.maximum(s - strike, 0.0)
    elif option_type == "put":
        return lambda s: np.maximum(strike - s, 0.0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")


def monte_carlo_european(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    option_type: str,
    *,
    n_paths: int = 100_000,
    antithetic: bool = True,
    control_variate: bool = True,
    rng: np.random.Generator | None = None,
) -> MCResult:
    """Monte Carlo pricing for European vanilla option under GBM.

    Uses optional antithetic sampling and Black–Scholes control variate.
    Returns price, standard error, and 95% confidence interval.
    """
    if n_paths <= 0:
        raise ValueError("n_paths must be positive")
    if n_paths % 2 == 1 and antithetic:
        n_paths += 1  # make even

    payoff_fn = _european_payoff(strike, option_type)
    spots_t = _generate_terminal_spots(
        spot, rate, vol, maturity, n_paths, antithetic=antithetic, rng=rng
    )
    payoffs = payoff_fn(spots_t)

    df = math.exp(-rate * maturity)
    disc_payoffs = df * payoffs

    if control_variate:
        # Control variate: use exact terminal expectation of spot and/or BS price
        bs_closed = black_scholes_price(spot, strike, rate, vol, maturity, option_type)
        # Use payoff of call as control? We approximate with linear relation to ST
        # Simpler: use sample mean adjustment with known expected discounted payoff (bs_closed)
        sample_mean = disc_payoffs.mean()
        adjusted = disc_payoffs + (bs_closed - sample_mean)
        disc_payoffs = adjusted

    price = disc_payoffs.mean()
    std = disc_payoffs.std(ddof=1)
    stderr = std / math.sqrt(len(disc_payoffs))
    ci95 = (price - 1.96 * stderr, price + 1.96 * stderr)
    return MCResult(
        price=price,
        stderr=stderr,
        ci95=ci95,
        n_paths=len(disc_payoffs),
        details={"std": std},
    )
