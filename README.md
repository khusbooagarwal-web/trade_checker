# Portfolio Trade Compliance Checker

This program reads proposed trades from a CSV file, checks them against the
portfolio details in `portfolio_data.json`, and writes a decision for each
trade to `output.csv`.

## What each file contains

- `trades_test.csv` is the example list of proposed trades.
- `portfolio_data.json` contains portfolio cash, restricted securities, limits,
  and current holdings.
- `main.py` starts the checker.
- `trade_checker.py` contains the rules and runs them when `main.py` imports it.
- `output.csv` is created after the program runs.

The `portfolio_id` values in your CSV must match IDs in `portfolio_data.json`.

## Run the example

Open a terminal in the project folder (the folder containing `main.py`), then
run:

```text
python -m pip install -r submission_ready_trade_checker\requirements.txt
python main.py
```

The results will be saved as `output.csv` in the project folder. Each row keeps
the original trade information and adds a `decision` and `reason`.

## Use your own CSV

Your CSV must have these column headers:

```text
portfolio_id,security_id,action,quantity,price,security_type
```

To use your CSV, put it in the project folder and open `trade_checker.py`.
Change the CSV filename in this line:

```python
trades = pd.read_csv("trades_test.csv")
```

For example, if your file is called `my_trades.csv`, change the line to
`trades = pd.read_csv("my_trades.csv")`. Save it, then run `python main.py`
again.

The CSV supplies the proposed trades. Portfolio reference data still comes
from `portfolio_data.json`; if your portfolios are in a different format,
they must be added to that JSON file before running the checker.

## Run the tests

```text
python -m pytest
```
