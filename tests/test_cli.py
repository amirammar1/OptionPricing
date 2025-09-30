import subprocess, sys

def run_cli(args):
    result = subprocess.run([sys.executable, '-m', 'option_pricing.cli'] + args, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_cli_bs():
    out = run_cli(['bs', '--spot', '100', '--strike', '100', '--rate', '0.01', '--vol', '0.2', '--maturity', '1', '--type', 'call'])
    assert 'Price' in out


def test_cli_mc():
    out = run_cli(['mc', '--spot', '100', '--strike', '100', '--rate', '0.01', '--vol', '0.2', '--maturity', '1', '--type', 'call', '--n-paths', '2000'])
    assert 'Monte Carlo Result' in out
