from bestsellers.analysis import findings, genre_engagement, price_change_pct
from bestsellers.clean import load
from bestsellers.plots import make_all


def test_findings(sample_csv):
    df = load(sample_csv)
    f = findings(df)
    assert f["years"] == "2009-2019"
    assert f["price_change_pct"] == price_change_pct(df)
    assert set(genre_engagement(df).index) == {"Fiction", "Non Fiction"}


def test_make_all_writes_seven_figures(sample_csv, tmp_path):
    paths = make_all(load(sample_csv), tmp_path)
    assert len(paths) == 7
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)
