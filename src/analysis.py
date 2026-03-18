"""
Higher-level analysis on top of the cleaned sales data.
"""

import pandas as pd


def monthly_growth(monthly: pd.DataFrame) -> pd.DataFrame:
    df = monthly.copy().sort_values("month")
    df["growth_pct"] = df["revenue"].pct_change() * 100
    return df


def category_ranking(category_df: pd.DataFrame) -> pd.DataFrame:
    return category_df.sort_values("revenue", ascending=False).reset_index(drop=True)


def payment_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("payment_method")
        .agg(revenue=("total_amount", "sum"), orders=("order_id", "count"))
        .assign(pct=lambda x: (x["orders"] / x["orders"].sum() * 100).round(1))
        .sort_values("orders", ascending=False)
        .reset_index()
    )


def region_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region")
        .agg(
            revenue=("total_amount", "sum"),
            orders=("order_id", "count"),
            customers=("customer_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index()
    )


def repeat_vs_new(df: pd.DataFrame) -> dict:
    order_counts = df.groupby("customer_id")["order_id"].count()
    repeat = (order_counts > 1).sum()
    new = (order_counts == 1).sum()
    return {
        "repeat_customers": int(repeat),
        "new_customers": int(new),
        "repeat_rate_pct": round(repeat / len(order_counts) * 100, 1),
    }


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return (
        df.groupby("product")
        .agg(
            revenue=("total_amount", "sum"),
            units=("quantity", "sum"),
            orders=("order_id", "count"),
        )
        .sort_values("revenue", ascending=False)
        .head(n)
        .reset_index()
    )
