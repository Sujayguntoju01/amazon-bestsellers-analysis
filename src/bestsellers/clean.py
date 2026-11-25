"""Load and clean the Amazon Top 50 bestsellers dataset."""
import re
from pathlib import Path

import pandas as pd

COLUMNS = {
    "Name": "title",
    "Author": "author",
    "User Rating": "rating",
    "Reviews": "reviews",
    "Price": "price",
    "Year": "year",
    "Genre": "genre",
}


def normalize_author(name: str) -> str:
    """Collapse spacing and initials so 'J. K. Rowling' and 'J.K. Rowling' match."""
    name = re.sub(r"\s+", " ", str(name)).strip()
    # "J. K." / "J.K." / "J. K" -> "J.K."
    name = re.sub(r"\b([A-Z])\.\s*(?=[A-Z]\.)", r"\1.", name)
    name = re.sub(r"\b([A-Z])\s+([A-Z])\b(?=\s)", r"\1.\2.", name)
    return name


def title_key(title: str) -> str:
    """Case/punctuation-insensitive key used to detect repeat titles."""
    return re.sub(r"[^a-z0-9]+", " ", str(title).lower()).strip()


def load(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path).rename(columns=COLUMNS)
    df["title"] = df["title"].str.strip()
    df["author"] = df["author"].map(normalize_author)
    df["genre"] = df["genre"].str.strip().str.title()
    df["year"] = df["year"].astype(int)
    return df


def unique_titles(df: pd.DataFrame) -> pd.DataFrame:
    """One row per book: titles that charted in several years are counted once.

    Keeps the most recent year's rating/reviews/price and records how many
    years the book appeared in the Top 50.
    """
    df = df.assign(title_key=df["title"].map(title_key))
    years = df.groupby("title_key")["year"].agg(first_year="min", last_year="max", years_on_list="nunique")
    latest = df.sort_values("year").groupby("title_key").tail(1).set_index("title_key")
    return latest.drop(columns="year").join(years).reset_index(drop=True)


def cleaning_report(raw: pd.DataFrame, clean: pd.DataFrame) -> dict:
    raw_authors = raw["Author"].str.strip().nunique() if "Author" in raw else None
    return {
        "rows": int(len(clean)),
        "authors_before": int(raw_authors) if raw_authors is not None else None,
        "authors_after": int(clean["author"].nunique()),
        "unique_titles": int(clean["title"].map(title_key).nunique()),
    }
