from option_pricing.analytics import greeks_summary
from option_pricing.models import MarketData, OptionSpec


def test_greeks_summary_keys():
    g = greeks_summary(100, 100, 0.01, 0.2, 1.0)
    assert "delta_call" in g and "gamma" in g


def test_models_validation():
    opt = OptionSpec(strike=100, maturity=1.0, option_type="call")
    mkt = MarketData(spot=100, rate=0.01, vol=0.2)
    assert opt.strike == 100 and mkt.spot == 100
    # invalid option type
    try:
        OptionSpec(strike=100, maturity=1.0, option_type="x")  # type: ignore[arg-type]
    except ValueError:
        pass
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError for invalid option type")
