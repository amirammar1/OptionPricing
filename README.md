# Option Pricing Library

Professional, well-tested Python library implementing Black–Scholes analytical formulas and Monte Carlo simulation engines for European (and extensible to path-dependent) options. Includes benchmarking, reproducibility, CLI, and examples.

## Features
- Black–Scholes closed-form pricing & Greeks (delta, gamma, vega, theta, rho)
- Monte Carlo pricing (European call/put) with variance reduction (antithetic, control variate vs. Black–Scholes)
- Convergence diagnostics & error estimates
- Clean architecture (core models, engines, analytics, CLI)
- Unit tests with `pytest`
- Benchmark script comparing MC vs analytical
- Typed code (PEP 484) + docstrings (NumPy style)
- Packaging via `pyproject.toml`

## Quick Start
```bash
# Create environment (Windows PowerShell)
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -e .[dev]

# Run tests
pytest -q

# CLI help
option-pricer --help
```

### Example (Python)
```python
from option_pricing.black_scholes import black_scholes_price
price = black_scholes_price(spot=100, strike=100, rate=0.05, vol=0.2, maturity=1.0, option_type="call")
print(price)
```

### Example (CLI)
```bash
option-pricer bs --spot 100 --strike 100 --rate 0.05 --vol 0.2 --maturity 1 --type call
```


## Benchmarks
Run:
```bash
python scripts/benchmark.py --spot 100 --strike 100 --rate 0.01 --vol 0.2 --maturity 1 --n 100000
```
Outputs pricing comparison, standard errors, and RMSE convergence.




