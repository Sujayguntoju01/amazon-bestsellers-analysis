"""The seven figures used in the analysis."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from .analysis import price_by_year, top_authors  # noqa: E402
from .clean import unique_titles  # noqa: E402

PALETTE = {"Fiction": "#2a6f97", "Non Fiction": "#e09f3e"}


def _save(fig, out_dir: Path, name: str) -> Path:
    path = out_dir / name
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def make_all(df: pd.DataFrame, out_dir: str | Path = "figures") -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    books = unique_titles(df)
    paths = []

    fig, ax = plt.subplots(figsize=(8, 4.5))
    price_by_year(df).plot(ax=ax, marker="o", color="#2a6f97")
    ax.set(title="Average bestseller price by year", xlabel="Year", ylabel="Average price ($)")
    paths.append(_save(fig, out_dir, "01_avg_price_by_year.png"))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    df.groupby(["year", "genre"]).size().unstack().plot(kind="bar", stacked=True, ax=ax,
                                                         color=PALETTE)
    ax.set(title="Fiction vs non-fiction in the Top 50", xlabel="Year", ylabel="Books")
    paths.append(_save(fig, out_dir, "02_genre_mix_by_year.png"))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.boxplot(data=books, x="genre", y="reviews", hue="genre", palette=PALETTE, ax=ax, legend=False)
    ax.set(title="Reader engagement: reviews per book (unique titles)", xlabel="", ylabel="Reviews")
    paths.append(_save(fig, out_dir, "03_reviews_by_genre.png"))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.histplot(data=books, x="rating", hue="genre", palette=PALETTE, multiple="stack", binwidth=0.1, ax=ax)
    ax.set(title="User rating distribution", xlabel="User rating", ylabel="Books")
    paths.append(_save(fig, out_dir, "04_rating_distribution.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    top_authors(df).sort_values().plot(kind="barh", ax=ax, color="#2a6f97")
    ax.set(title="Authors with the most Top 50 appearances", xlabel="Appearances", ylabel="")
    paths.append(_save(fig, out_dir, "05_top_authors.png"))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.violinplot(data=books, x="genre", y="price", hue="genre", palette=PALETTE, cut=0, ax=ax, legend=False)
    ax.set(title="Price distribution by genre", xlabel="", ylabel="Price ($)")
    paths.append(_save(fig, out_dir, "06_price_by_genre.png"))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.scatterplot(data=books, x="reviews", y="rating", hue="genre", palette=PALETTE, alpha=0.7, ax=ax)
    ax.set(title="Do more reviews mean higher ratings?", xlabel="Reviews", ylabel="User rating", xscale="log")
    paths.append(_save(fig, out_dir, "07_rating_vs_reviews.png"))

    return paths
