from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from .black_scholes import black_scholes_greeks, black_scholes_price
from .monte_carlo import monte_carlo_european

console = Console()

def _common_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--spot", type=float, required=True)
    parser.add_argument("--strike", type=float, required=True)
    parser.add_argument("--rate", type=float, required=True)
    parser.add_argument("--vol", type=float, required=True)
    parser.add_argument("--maturity", type=float, required=True)
    parser.add_argument("--type", dest="option_type", choices=["call", "put"], required=True)


def cmd_bs(args: argparse.Namespace) -> None:
    price = black_scholes_price(
        args.spot, args.strike, args.rate, args.vol, args.maturity, args.option_type
    )
    greeks = black_scholes_greeks(
        args.spot, args.strike, args.rate, args.vol, args.maturity
    )
    table = Table(title="Black–Scholes Result")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Price", f"{price:.6f}")
    for k, v in greeks.items():
        table.add_row(k, f"{v:.6f}")
    console.print(table)


def cmd_mc(args: argparse.Namespace) -> None:
    result = monte_carlo_european(
        spot=args.spot,
        strike=args.strike,
        rate=args.rate,
        vol=args.vol,
        maturity=args.maturity,
        option_type=args.option_type,
        n_paths=args.n_paths,
        antithetic=not args.no_antithetic,
        control_variate=not args.no_cv,
    )
    table = Table(title="Monte Carlo Result")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Price", f"{result.price:.6f}")
    table.add_row("StdErr", f"{result.stderr:.6f}")
    table.add_row("CI95 Low", f"{result.ci95[0]:.6f}")
    table.add_row("CI95 High", f"{result.ci95[1]:.6f}")
    console.print(table)


def cmd_compare(args: argparse.Namespace) -> None:
    from math import fabs

    bs = black_scholes_price(
        args.spot, args.strike, args.rate, args.vol, args.maturity, args.option_type
    )
    mc = monte_carlo_european(
        args.spot,
        args.strike,
        args.rate,
        args.vol,
        args.maturity,
        args.option_type,
        n_paths=args.n_paths,
    ).price
    table = Table(title="BS vs MC Comparison")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Black–Scholes", f"{bs:.6f}")
    table.add_row("Monte Carlo", f"{mc:.6f}")
    table.add_row("Abs Diff", f"{fabs(bs-mc):.6f}")
    console.print(table)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="option-pricer", description="Option pricing tools")
    sub = parser.add_subparsers(dest="command", required=True)

    p_bs = sub.add_parser("bs", help="Black–Scholes pricing")
    _common_parser(p_bs)
    p_bs.set_defaults(func=cmd_bs)

    p_mc = sub.add_parser("mc", help="Monte Carlo pricing")
    _common_parser(p_mc)
    p_mc.add_argument("--n-paths", type=int, default=100000)
    p_mc.add_argument("--no-antithetic", action="store_true")
    p_mc.add_argument("--no-cv", action="store_true", help="Disable control variate")
    p_mc.set_defaults(func=cmd_mc)

    p_cmp = sub.add_parser("compare", help="Compare BS vs MC")
    _common_parser(p_cmp)
    p_cmp.add_argument("--n-paths", type=int, default=100000)
    p_cmp.set_defaults(func=cmd_compare)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":  # pragma: no cover
    main()
