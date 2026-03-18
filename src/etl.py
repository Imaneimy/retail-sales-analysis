"""
Load and clean raw sales data.
"""

import pandas as pd
from pathlib import Path


def load_sales(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["order_id", "customer_id", "total_amount", "order_date"])
    df = df[df["total_amount"] > 0]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 45, 60, 100],
        labels=["<25", "25-35", "35-45", "45-60", "60+"],
    )
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Replicate the top-level KPIs from the Power BI dashboard:
    Total Sales, Average Order Value, number of transactions, unique customers.
    """
    return {
        "total_sales": round(df["total_amount"].sum(), 2),
        "aov": round(df["total_amount"].mean(), 2),
        "transactions": len(df),
        "unique_customers": df["customer_id"].nunique(),
    }


def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("month")
        .agg(revenue=("total_amount", "sum"), orders=("order_id", "count"))
        .reset_index()
        .sort_values("month")
    )


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category")
        .agg(revenue=("total_amount", "sum"), orders=("order_id", "count"))
        .assign(pct=lambda x: (x["revenue"] / x["revenue"].sum() * 100).round(1))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )


def sales_by_gender_age(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["gender", "age_group"])
        .agg(revenue=("total_amount", "sum"), customers=("customer_id", "nunique"))
        .reset_index()
    )


def top_customers(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby(["customer_id", "customer_name"])
        .agg(
            total_spent=("total_amount", "sum"),
            orders=("order_id", "count"),
            last_order=("order_date", "max"),
        )
        .sort_values("total_spent", ascending=False)
        .head(n)
        .reset_index()
    )
