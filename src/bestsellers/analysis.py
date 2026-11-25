"""Key findings computed from the cleaned data."""
import pandas as pd

from .clean import unique_titles


def price_by_year(df: pd.DataFrame) -> pd.Series:
    return df.groupby("year")["price"].mean().round(2)


def price_change_pct(df: pd.DataFrame) -> float:
    """% change in average price between the first and last year."""
    by_year = price_by_year(df)
    return round((by_year.iloc[-1] - by_year.iloc[0]) / by_year.iloc[0] * 100, 1)


def genre_engagement(df: pd.DataFrame) -> pd.DataFrame:
    """Reviews per book by genre, on unique titles to avoid double-counting."""
    books = unique_titles(df)
    return (
        books.groupby("genre")
        .agg(books=("title", "count"), median_reviews=("reviews", "median"),
             mean_reviews=("reviews", "mean"), mean_rating=("rating", "mean"))
        .round(2)
    )


def top_authors(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df["author"].value_counts().head(n)


def findings(df: pd.DataFrame) -> dict:
    eng = genre_engagement(df)
    by_year = price_by_year(df)
    return {
        "rows": int(len(df)),
        "unique_titles": int(len(unique_titles(df))),
        "years": f"{df['year'].min()}-{df['year'].max()}",
        "avg_price_first_year": float(by_year.iloc[0]),
        "avg_price_last_year": float(by_year.iloc[-1]),
        "price_change_pct": float(price_change_pct(df)),
        "median_reviews_by_genre": {g: float(v) for g, v in eng["median_reviews"].items()},
        "fiction_share_pct": round(float((df["genre"] == "Fiction").mean() * 100), 1),
        "top_author": df["author"].value_counts().index[0],
    }
