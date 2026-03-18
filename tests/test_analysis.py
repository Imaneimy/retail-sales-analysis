import sys
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from etl import load_sales, sales_by_month, sales_by_category
from analysis import monthly_growth, payment_breakdown, region_summary, repeat_vs_new, top_products

DATA = Path(__file__).parent.parent / "data" / "sales_data.csv"


@pytest.fixture(scope="module")
def df():
    return load_sales(DATA)


# TC-ANA-001
def test_monthly_growth_has_growth_col(df):
    monthly = sales_by_month(df)
    growth = monthly_growth(monthly)
    assert "growth_pct" in growth.columns


# TC-ANA-002
def test_monthly_growth_first_row_is_nan(df):
    monthly = sales_by_month(df)
    growth = monthly_growth(monthly)
    assert pd.isna(growth["growth_pct"].iloc[0])


# TC-ANA-003
def test_payment_breakdown_sums_to_100(df):
    pb = payment_breakdown(df)
    assert abs(pb["pct"].sum() - 100.0) < 0.5


# TC-ANA-004
def test_region_summary_contains_all_regions(df):
    expected = set(df["region"].unique())
    result = set(region_summary(df)["region"])
    assert expected == result


# TC-ANA-005
def test_region_summary_sorted_descending(df):
    rs = region_summary(df)
    revenues = rs["revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)


# TC-ANA-006
def test_repeat_vs_new_keys(df):
    result = repeat_vs_new(df)
    for k in ["repeat_customers", "new_customers", "repeat_rate_pct"]:
        assert k in result


# TC-ANA-007
def test_repeat_vs_new_totals_match(df):
    result = repeat_vs_new(df)
    assert result["repeat_customers"] + result["new_customers"] == df["customer_id"].nunique()


# TC-ANA-008
def test_top_products_default_limit(df):
    assert len(top_products(df)) <= 5


# TC-ANA-009
def test_top_products_sorted(df):
    tp = top_products(df)
    revenues = tp["revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)


# TC-ANA-010
def test_top_products_custom_limit(df):
    tp = top_products(df, n=3)
    assert len(tp) <= 3
