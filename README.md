# IMC Prosperity 4 Backtester

[![Build Status](https://github.com/rkothari3/IMC_P4_Backtester/actions/workflows/build.yml/badge.svg)](https://github.com/rkothari3/IMC_P4_Backtester/actions/workflows/build.yml)

Backtester for [IMC Prosperity 4](https://prosperity.imc.com/) algorithms.

## Installation

```sh
pip install imc_p4_bt
```

## Usage

```sh
# Backtest on all days from round 1
$ imc-p4-bt example/starter.py 1

# Backtest on round 1 day 0
$ imc-p4-bt example/starter.py 1-0

# Backtest on round 1 day -1 and round 1 day 0
$ imc-p4-bt example/starter.py 1--1 1-0

# Backtest on all days from rounds 1 and 2
$ imc-p4-bt example/starter.py 1 2

# Merge profit and loss across days
$ imc-p4-bt example/starter.py 1 --merge-pnl

# Automatically open the result in the visualizer when done
$ imc-p4-bt example/starter.py 1 --vis

# Write algorithm output to custom file
$ imc-p4-bt example/starter.py 1 --out example.log

# Skip saving the output log to a file
$ imc-p4-bt example/starter.py 1 --no-out

# Backtest on custom data
$ imc-p4-bt example/starter.py 1 --data prosperity4bt/resources

# Print trader's output to stdout while running
$ imc-p4-bt example/starter.py 1 --print
```

## Order Matching

Orders placed by `Trader.run` at a given timestamp are matched against the order depths and market trades of that timestamp's state. Order depths take priority — if an order can be filled completely using volume in the relevant order depth, market trades are not considered. If not, the backtester matches your order against the timestamp's market trades.

Market trades are matched at the price of your orders, e.g. if you place a sell order for €9 and there is a market trade for €10, the sell order is matched at €9.

Matching behavior is configurable via `--match-trades`:
- `--match-trades all` (default): match market trades with prices equal to or worse than your quotes.
- `--match-trades worse`: match market trades with prices strictly worse than your quotes.
- `--match-trades none`: do not match market trades against orders.

Limits are enforced before orders are matched. If your position would exceed the limit assuming all orders fill, all orders for that product are canceled.

### Position Limits

Known Prosperity 4 products are defined in `prosperity4bt/data.py` (`LIMITS`).

| Round | Product | Limit |
|-------|---------|-------|
| 0 | `EMERALDS` | 80 |
| 0 | `TOMATOES` | 80 |
| 1 | `ASH_COATED_OSMIUM` | 80 |
| 1 | `INTARIAN_PEPPER_ROOT` | 80 |

Any unlisted product defaults to **50**. Override limits without editing code:

```sh
imc-p4-bt sample.py 0 --limit EMERALDS:80 --limit TOMATOES:80
```

## Data Files

Data files are bundled for rounds 0, 1, and 2. More will be added as rounds are released.

Conversions are not supported.

## Environment Variables

During backtests, two environment variables are set:
- `PROSPERITY4BT_ROUND` — the round number
- `PROSPERITY4BT_DAY` — the day number

These do not exist in the official submission environment — do not rely on them in submitted code.

## Development

```sh
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up
git clone https://github.com/rkothari3/IMC_P4_Backtester
cd IMC_P4_Backtester
uv venv && source .venv/bin/activate
uv sync
```

Changes are automatically reflected the next time you run `imc-p4-bt` inside the venv.
