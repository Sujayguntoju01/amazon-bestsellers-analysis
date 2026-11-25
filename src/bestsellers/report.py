"""Clean the data, compute findings and write all figures.

Usage: python -m bestsellers.report --data "data/bestsellers with categories.csv"
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from .analysis import findings
from .clean import cleaning_report, load
from .plots import make_all


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data/bestsellers with categories.csv")
    parser.add_argument("--out", default="figures")
    args = parser.parse_args()

    raw = pd.read_csv(args.data)
    df = load(args.data)
    result = {"cleaning": cleaning_report(raw, df), "findings": findings(df)}
    paths = make_all(df, args.out)
    Path(args.out, "findings.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print(f"\nSaved {len(paths)} figures to {args.out}/")


if __name__ == "__main__":
    main()
