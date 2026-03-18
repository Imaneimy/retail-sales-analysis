# retail-sales-analysis

This project started as a Power BI dashboard I built to analyze retail sales across France and Morocco — tracking revenue trends, category performance, and customer segments. I've since rebuilt it in Python so it's reproducible, testable, and easier to extend.

The dataset covers 40 orders from Q1 2024 across six product categories and eight cities (Paris, Casablanca, Rabat, Marrakech, Lyon, Marseille, Bordeaux). The pipeline cleans the raw CSV, computes KPIs, runs segmentation by category/region/age/gender, and outputs five Matplotlib charts.

## Structure

```
src/
  etl.py              # load, clean, feature engineering (month, age_group)
  analysis.py         # monthly growth, region summary, repeat vs new customers
  visualizations.py   # five Matplotlib charts saved to reports/
  run_analysis.py     # entry point

tests/
  test_etl.py         # 15 unit tests TC-RET-001→015
  test_analysis.py    # 10 unit tests TC-ANA-001→010

data/
  sales_data.csv      # 40 orders, Q1 2024

reports/              # generated charts (git-ignored)
```

## Running it

```bash
pip install -r requirements.txt
cd src
python run_analysis.py
```

This prints the KPI summary, monthly growth table, top customers, and saves five charts to `reports/`.

```bash
pytest tests/ -v
```

## Key metrics computed

- Total sales, AOV, transaction count, unique customers
- Month-over-month revenue growth
- Revenue and order share by category (with % breakdown)
- Revenue by region and by age group / gender
- Repeat vs new customer rate
- Top 10 customers by spend, top 5 products by revenue

## Stack

Python, Pandas, Matplotlib, Pytest
