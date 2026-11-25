# Amazon Bestsellers Analysis (2009–2019)

[![CI](https://github.com/Sujayguntoju01/amazon-bestsellers-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/Sujayguntoju01/amazon-bestsellers-analysis/actions/workflows/ci.yml)

Exploratory analysis of **550 Amazon Top 50 bestsellers** from 2009–2019: how prices changed, whether readers engage more with fiction or non-fiction, and which authors dominate the list.

Built with **Python, pandas, Matplotlib, Seaborn and Jupyter**.

## Key findings

| Question | Finding |
|---|---|
| Did prices change? | Average price fell from **$15.40** (2009) to **$10.08** (2019), a **34.5% decline** |
| Fiction vs non-fiction engagement | Fiction titles get a median of **8,840 reviews** vs **4,955** for non-fiction (**~78% more**) |
| Genre mix | Fiction makes up **43.6%** of all Top 50 slots |
| Who charts most? | **Jeff Kinney** (Diary of a Wimpy Kid) |
| Data quality | 2 duplicate author spellings merged (248 → 246 authors); 550 rows collapse to **350 unique titles** |

![Average price by year](figures/01_avg_price_by_year.png)

## Data cleaning

Two issues in the raw data would distort the results:

1. **Inconsistent author names.** The same author is spelled with different spacing in their initials (e.g. `J. K. Rowling` vs `J.K. Rowling`, `George R. R. Martin` vs `George R.R. Martin`), which splits their counts. `normalize_author()` collapses these variants.
2. **Repeat titles.** Many books appear in several years' Top 50. Comparing genres row by row would count long-running titles many times, so genre and engagement comparisons use `unique_titles()`, which keeps one row per book and records how many years it charted.

## Visualizations

| # | Figure | Question |
|---|---|---|
| 1 | `01_avg_price_by_year.png` | How did average price change? |
| 2 | `02_genre_mix_by_year.png` | Fiction vs non-fiction share per year |
| 3 | `03_reviews_by_genre.png` | Which genre gets more reader engagement? |
| 4 | `04_rating_distribution.png` | How are user ratings distributed? |
| 5 | `05_top_authors.png` | Which authors chart most often? |
| 6 | `06_price_by_genre.png` | Do genres differ in price? |
| 7 | `07_rating_vs_reviews.png` | Do more reviews mean higher ratings? |

## Run it

```bash
git clone https://github.com/Sujayguntoju01/amazon-bestsellers-analysis.git
cd amazon-bestsellers-analysis
pip install -r requirements-dev.txt

./scripts/download_data.sh                    # needs a Kaggle API token
PYTHONPATH=src python -m bestsellers.report   # findings + 7 figures in figures/
jupyter notebook notebooks/analysis.ipynb     # full walkthrough
```

## Project structure

```
├── notebooks/analysis.ipynb    step-by-step analysis
├── src/bestsellers/
│   ├── clean.py                author normalization, de-duplication
│   ├── analysis.py             price trend, genre engagement, top authors
│   ├── plots.py                the 7 figures
│   └── report.py               CLI: findings.json + figures
├── tests/                      pytest (runs on a synthetic sample in CI)
└── figures/                    generated charts
```

## Tests

```bash
ruff check . && pytest -q
```
