"""
Entry point: load data, run analysis, generate charts.
"""

from pathlib import Path
from etl import load_sales, compute_kpis, sales_by_month, sales_by_category, sales_by_gender_age, top_customers
from analysis import monthly_growth, payment_breakdown, region_summary, repeat_vs_new, top_products
from visualizations import (
    plot_monthly_revenue,
    plot_category_share,
    plot_gender_age_revenue,
    plot_region_revenue,
    plot_top_products,
)

DATA = Path(__file__).parent.parent / "data" / "sales_data.csv"
REPORTS = Path(__file__).parent.parent / "reports"
REPORTS.mkdir(exist_ok=True)


def main():
    df = load_sales(DATA)

    kpis = compute_kpis(df)
    print("\n--- KPIs ---")
    for k, v in kpis.items():
        print(f"  {k}: {v}")

    monthly = sales_by_month(df)
    growth = monthly_growth(monthly)
    print("\n--- Monthly revenue with growth ---")
    print(growth.to_string(index=False))

    categories = sales_by_category(df)
    print("\n--- Revenue by category ---")
    print(categories.to_string(index=False))

    regions = region_summary(df)
    print("\n--- Revenue by region ---")
    print(regions.to_string(index=False))

    print("\n--- Repeat vs new customers ---")
    print(repeat_vs_new(df))

    print("\n--- Top 5 products ---")
    print(top_products(df).to_string(index=False))

    print("\n--- Top 10 customers ---")
    print(top_customers(df).to_string(index=False))

    plot_monthly_revenue(monthly, str(REPORTS / "monthly_revenue.png"))
    plot_category_share(categories, str(REPORTS / "category_share.png"))
    plot_gender_age_revenue(sales_by_gender_age(df), str(REPORTS / "gender_age_revenue.png"))
    plot_region_revenue(regions, str(REPORTS / "region_revenue.png"))
    plot_top_products(top_products(df), str(REPORTS / "top_products.png"))

    print(f"\nCharts saved to {REPORTS}/")


if __name__ == "__main__":
    main()
