from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_european

def test_mc_converges_basic():
    bs = black_scholes_price(100, 100, 0.01, 0.2, 1.0, "call")
    result = monte_carlo_european(100, 100, 0.01, 0.2, 1.0, "call", n_paths=50_000)
    assert abs(result.price - bs) < 0.01  # within 1 cent typical with 50k paths
