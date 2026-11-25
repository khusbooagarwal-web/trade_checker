import subprocess
import sys
from pathlib import Path

import pandas as pd


def test_checker_creates_decision_for_each_trade():
    project_folder = Path(__file__).resolve().parent
    subprocess.run(
        [sys.executable, "main.py"],
        cwd=project_folder,
        check=True,
    )

    results = pd.read_csv(project_folder / "output.csv")

    trades = pd.read_csv(project_folder / "trades_test.csv")
    assert len(results) == len(trades)
    assert "decision" in results.columns
    assert "reason" in results.columns
    assert results.loc[6, "reason"] == "Invalid trade data."
