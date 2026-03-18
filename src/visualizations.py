"""
Matplotlib charts for the sales analysis.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from pathlib import Path


def _save(fig: plt.Figure, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)


def plot_monthly_revenue(monthly: pd.DataFrame, out: str = "reports/monthly_revenue.png") -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(monthly["month"], monthly["revenue"], color="#4C72B0")
    ax.set_title("Monthly Revenue", fontsize=14, pad=12)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (€)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.xticks(rotation=30, ha="right")
    _save(fig, out)


def plot_category_share(category_df: pd.DataFrame, out: str = "reports/category_share.png") -> None:
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        category_df["revenue"],
        labels=category_df["category"],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"],
    )
    ax.set_title("Revenue by Category", fontsize=14, pad=12)
    _save(fig, out)


def plot_gender_age_revenue(gender_age: pd.DataFrame, out: str = "reports/gender_age_revenue.png") -> None:
    pivot = gender_age.pivot_table(index="age_group", columns="gender", values="revenue", aggfunc="sum").fillna(0)
    fig, ax = plt.subplots(figsize=(9, 5))
    pivot.plot(kind="bar", ax=ax, color=["#DD8452", "#4C72B0"])
    ax.set_title("Revenue by Age Group and Gender", fontsize=14, pad=12)
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Revenue (€)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.xticks(rotation=0)
    ax.legend(title="Gender")
    _save(fig, out)


def plot_region_revenue(region_df: pd.DataFrame, out: str = "reports/region_revenue.png") -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(region_df["region"], region_df["revenue"], color="#55A868")
    ax.set_title("Revenue by Region", fontsize=14, pad=12)
    ax.set_xlabel("Revenue (€)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.invert_yaxis()
    _save(fig, out)


def plot_top_products(products: pd.DataFrame, out: str = "reports/top_products.png") -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(products["product"], products["revenue"], color="#C44E52")
    ax.set_title("Top 5 Products by Revenue", fontsize=14, pad=12)
    ax.set_xlabel("Revenue (€)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.invert_yaxis()
    _save(fig, out)
