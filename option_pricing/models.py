from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class OptionSpec:
    """Specification of a European vanilla option."""
    strike: float
    maturity: float  # in years
    option_type: str  # 'call' or 'put'

    def __post_init__(self) -> None:
        if self.option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")
        if self.strike <= 0:
            raise ValueError("strike must be positive")
        if self.maturity <= 0:
            raise ValueError("maturity must be positive")

@dataclass(frozen=True, slots=True)
class MarketData:
    spot: float
    rate: float  # continuously compounded risk-free rate
    vol: float   # implied volatility

    def __post_init__(self) -> None:
        if self.spot <= 0:
            raise ValueError("spot must be positive")
        if self.vol <= 0:
            raise ValueError("vol must be positive")
