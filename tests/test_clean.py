import pytest

from bestsellers.clean import load, normalize_author, title_key, unique_titles


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("J. K. Rowling", "J.K. Rowling"),
        ("J.K. Rowling", "J.K. Rowling"),
        ("George R. R. Martin", "George R.R. Martin"),
        ("  Suzanne   Collins ", "Suzanne Collins"),
        ("Dr. Seuss", "Dr. Seuss"),
    ],
)
def test_normalize_author(raw, expected):
    assert normalize_author(raw) == expected


def test_title_key_ignores_case_and_punctuation():
    assert title_key("The Hunger Games!") == title_key("the hunger games")


def test_load_merges_author_variants(sample_csv):
    df = load(sample_csv)
    assert "J. K. Rowling" not in set(df["author"])
    assert len(df) == 550
    assert set(df["genre"]) == {"Fiction", "Non Fiction"}


def test_unique_titles_counts_each_book_once(sample_csv):
    df = load(sample_csv)
    books = unique_titles(df)
    assert books["title"].map(title_key).is_unique
    assert len(books) < len(df)
    assert books["years_on_list"].max() > 1
