#!/usr/bin/env python
from __future__ import annotations

import argparse
import math

import numpy as np

from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_european


def run(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n: int,
    steps: int,
) -> None:
    bs = black_scholes_price(spot, strike, rate, vol, maturity, "call")
    print(f"Black–Scholes call: {bs:.6f}")
    # Ensure unique sorted integer path counts
    path_grid = np.unique(
        np.round(np.logspace(math.log10(1_000), math.log10(n), steps)).astype(int)
    )
    for m in path_grid:
        result = monte_carlo_european(spot, strike, rate, vol, maturity, "call", n_paths=int(m))
        err = abs(result.price - bs)
        print(
            f"paths={int(m):>8d} price={result.price:.6f} stderr={result.stderr:.6f} "
            f"abs_err={err:.6f}"
        )


def parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Benchmark MC vs Black–Scholes")
    p.add_argument("--spot", type=float, required=True)
    p.add_argument("--strike", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--vol", type=float, required=True)
    p.add_argument("--maturity", type=float, required=True)
    p.add_argument("--n", type=int, default=200_000)
    p.add_argument("--steps", type=int, default=5)
    return p.parse_args()


if __name__ == "__main__":
    args = parse()
    run(args.spot, args.strike, args.rate, args.vol, args.maturity, args.n, args.steps)
