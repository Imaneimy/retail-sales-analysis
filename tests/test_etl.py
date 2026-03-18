"""
Unit tests for etl.py — mirrors the kind of checks I ran manually
when validating Power BI data against the source CSV at Orange Maroc.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from etl import load_sales, compute_kpis, sales_by_month, sales_by_category, sales_by_gender_age, top_customers

DATA = Path(__file__).parent.parent / "data" / "sales_data.csv"


@pytest.fixture(scope="module")
def df():
    return load_sales(DATA)


# TC-RET-001
def test_load_returns_dataframe(df):
    assert isinstance(df, pd.DataFrame)


# TC-RET-002
def test_no_duplicates(df):
    assert df["order_id"].duplicated().sum() == 0


# TC-RET-003
def test_no_null_critical_columns(df):
    for col in ["order_id", "customer_id", "total_amount", "order_date"]:
        assert df[col].isna().sum() == 0


# TC-RET-004
def test_all_amounts_positive(df):
    assert (df["total_amount"] > 0).all()


# TC-RET-005
def test_month_column_created(df):
    assert "month" in df.columns
    assert df["month"].str.match(r"\d{4}-\d{2}").all()


# TC-RET-006
def test_age_group_column_created(df):
    assert "age_group" in df.columns
    assert df["age_group"].isna().sum() == 0


# TC-RET-007
def test_kpis_keys(df):
    kpis = compute_kpis(df)
    for key in ["total_sales", "aov", "transactions", "unique_customers"]:
        assert key in kpis


# TC-RET-008
def test_kpi_total_matches_sum(df):
    kpis = compute_kpis(df)
    assert abs(kpis["total_sales"] - df["total_amount"].sum()) < 0.01


# TC-RET-009
def test_sales_by_month_row_count(df):
    monthly = sales_by_month(df)
    expected_months = df["month"].nunique()
    assert len(monthly) == expected_months


# TC-RET-010
def test_sales_by_month_sorted(df):
    monthly = sales_by_month(df)
    assert list(monthly["month"]) == sorted(monthly["month"].tolist())


# TC-RET-011
def test_sales_by_category_has_pct(df):
    cats = sales_by_category(df)
    assert "pct" in cats.columns
    assert abs(cats["pct"].sum() - 100.0) < 0.5


# TC-RET-012
def test_sales_by_category_sorted_descending(df):
    cats = sales_by_category(df)
    revenues = cats["revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)


# TC-RET-013
def test_gender_age_groups(df):
    ga = sales_by_gender_age(df)
    assert set(ga["gender"]).issubset({"F", "M"})


# TC-RET-014
def test_top_customers_default_limit(df):
    top = top_customers(df)
    assert len(top) <= 10


# TC-RET-015
def test_top_customers_sorted_by_spend(df):
    top = top_customers(df)
    spends = top["total_spent"].tolist()
    assert spends == sorted(spends, reverse=True)
