"""Synthetic stand-in with the same columns as the Kaggle file, for tests/CI only.

Usage: python scripts/make_sample_data.py --out data/sample.csv
"""
import argparse

import numpy as np
import pandas as pd

AUTHORS = ["J. K. Rowling", "J.K. Rowling", "George R. R. Martin", "George R.R. Martin",
           "Suzanne Collins", "Rick Riordan", "Jeff Kinney", "Gary Chapman", "Dr. Seuss",
           "American Psychological Association", "Stephenie Meyer", "Bill O'Reilly"]


def make(seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    titles = [f"Book {i}" for i in range(350)]
    for year in range(2009, 2020):
        for title in rng.choice(titles, 50, replace=False):
            genre = "Fiction" if int(title.split()[1]) % 2 else "Non Fiction"
            base = 18 - (year - 2009) * 0.6
            rows.append({
                "Name": title if rng.random() > 0.05 else f"  {title} ",
                "Author": rng.choice(AUTHORS),
                "User Rating": round(float(np.clip(rng.normal(4.6, 0.2), 3.3, 4.9)), 1),
                "Reviews": int(rng.lognormal(9.3 if genre == "Fiction" else 8.9, 0.8)),
                "Price": max(int(rng.normal(base, 5)), 0),
                "Year": year,
                "Genre": genre,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/sample.csv")
    args = parser.parse_args()
    make().to_csv(args.out, index=False)
    print(f"Wrote synthetic sample to {args.out}")
