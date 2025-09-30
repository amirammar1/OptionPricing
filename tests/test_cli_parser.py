from option_pricing.cli import build_parser


def test_build_parser_commands():
    parser = build_parser()
    # Simulate parsing a BS command
    args = parser.parse_args([
        "bs",
        "--spot",
        "100",
        "--strike",
        "100",
        "--rate",
        "0.01",
        "--vol",
        "0.2",
        "--maturity",
        "1",
        "--type",
        "call",
    ])
    assert args.command == "bs"
