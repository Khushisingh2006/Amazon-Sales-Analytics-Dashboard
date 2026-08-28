"""
analyze_kpis.py
Loads the sales dataset, computes 15+ business KPIs (revenue, profit,
customer & product trends), prints a summary, saves a JSON KPI file
(consumed by the HTML dashboard), and renders chart images into /images
for use in the README.

Run:
    python scripts/analyze_kpis.py
"""

import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"

df = pd.read_csv("data/amazon_sales_data.csv", parse_dates=["Order_Date"])
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
df["Year"] = df["Order_Date"].dt.year
df["Weekday"] = df["Order_Date"].dt.day_name()

kpis = {}

# 1-6: Core financial KPIs
kpis["total_revenue"] = round(df["Net_Sales"].sum(), 2)
kpis["total_profit"] = round(df["Profit"].sum(), 2)
kpis["profit_margin_pct"] = round(kpis["total_profit"] / kpis["total_revenue"] * 100, 2)
kpis["total_orders"] = int(df["Order_ID"].nunique())
kpis["avg_order_value"] = round(kpis["total_revenue"] / kpis["total_orders"], 2)
kpis["total_units_sold"] = int(df["Quantity"].sum())

# 7-8: Customers
kpis["unique_customers"] = int(df["Customer_ID"].nunique())
kpis["avg_revenue_per_customer"] = round(kpis["total_revenue"] / kpis["unique_customers"], 2)

# 9: Returns
kpis["return_rate_pct"] = round(df["Is_Returned"].mean() * 100, 2)

# 10: Avg rating
kpis["avg_customer_rating"] = round(df["Customer_Rating"].mean(), 2)

# 11: Avg discount
kpis["avg_discount_pct"] = round(df["Discount_Percent"].mean(), 2)

# 12: Top category by revenue
cat_rev = df.groupby("Category")["Net_Sales"].sum().sort_values(ascending=False)
kpis["top_category"] = cat_rev.index[0]
kpis["top_category_revenue"] = round(cat_rev.iloc[0], 2)

# 13: Top product
prod_rev = df.groupby("Product_Name")["Net_Sales"].sum().sort_values(ascending=False)
kpis["top_product"] = prod_rev.index[0]

# 14: Top state
state_rev = df.groupby("State")["Net_Sales"].sum().sort_values(ascending=False)
kpis["top_state"] = state_rev.index[0]

# 15: Best sales channel
channel_rev = df.groupby("Sales_Channel")["Net_Sales"].sum().sort_values(ascending=False)
kpis["top_sales_channel"] = channel_rev.index[0]

# 16: Best payment mode
pay_rev = df["Payment_Mode"].value_counts()
kpis["top_payment_mode"] = pay_rev.index[0]

# 17: YoY growth (2023 vs 2022, 2024 vs 2023)
yearly = df.groupby("Year")["Net_Sales"].sum()
yoy = {}
years = sorted(yearly.index)
for i in range(1, len(years)):
    prev, cur = years[i - 1], years[i]
    growth = round((yearly[cur] - yearly[prev]) / yearly[prev] * 100, 2)
    yoy[f"{prev}_to_{cur}"] = growth
kpis["yoy_growth_pct"] = yoy

# 18: Prime member share of revenue
seg_rev = df.groupby("Customer_Segment")["Net_Sales"].sum()
kpis["prime_member_revenue_share_pct"] = round(seg_rev.get("Prime Member", 0) / kpis["total_revenue"] * 100, 2)

# ---- Series for charts / dashboard ----
monthly_rev = df.groupby("Month")["Net_Sales"].sum().round(2)
monthly_profit = df.groupby("Month")["Profit"].sum().round(2)
category_series = cat_rev.round(2)
state_series = state_rev.head(10).round(2)
channel_series = channel_rev.round(2)
payment_series = df["Payment_Mode"].value_counts()
segment_series = seg_rev.round(2)
weekday_series = df.groupby("Weekday")["Net_Sales"].sum().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).round(2)
top_products_series = prod_rev.head(10).round(2)

dashboard_data = {
    "kpis": kpis,
    "monthly_revenue": {"labels": list(monthly_rev.index), "values": list(monthly_rev.values)},
    "monthly_profit": {"labels": list(monthly_profit.index), "values": list(monthly_profit.values)},
    "category_revenue": {"labels": list(category_series.index), "values": list(category_series.values)},
    "state_revenue": {"labels": list(state_series.index), "values": list(state_series.values)},
    "channel_revenue": {"labels": list(channel_series.index), "values": list(channel_series.values)},
    "payment_mode": {"labels": list(payment_series.index), "values": list(payment_series.values.astype(float))},
    "segment_revenue": {"labels": list(segment_series.index), "values": list(segment_series.values)},
    "weekday_revenue": {"labels": list(weekday_series.index), "values": list(weekday_series.values)},
    "top_products": {"labels": list(top_products_series.index), "values": list(top_products_series.values)},
}

with open("dashboard/dashboard_data.json", "w") as f:
    json.dump(dashboard_data, f, indent=2)

with open("docs/kpi_summary.json", "w") as f:
    json.dump(kpis, f, indent=2, default=str)

print("===== KEY PERFORMANCE INDICATORS =====")
for k, v in kpis.items():
    print(f"{k}: {v}")

# ----------------------------------------------------------------------
# Charts (saved to /images for README embedding)
# ----------------------------------------------------------------------
COLORS = ["#FF9900", "#146EB4", "#232F3E", "#37475A", "#FFA41C", "#00A8E1", "#7FBA00", "#F2B01E"]

plt.figure(figsize=(10, 5))
plt.plot(monthly_rev.index, monthly_rev.values, marker="o", color="#FF9900", linewidth=2)
plt.xticks(rotation=60, fontsize=7)
plt.title("Monthly Revenue Trend", fontsize=13, fontweight="bold")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig("images/monthly_revenue_trend.png", dpi=140)
plt.close()

plt.figure(figsize=(8, 5))
plt.barh(category_series.index[::-1], category_series.values[::-1], color="#146EB4")
plt.title("Revenue by Category", fontsize=13, fontweight="bold")
plt.xlabel("Revenue (₹)")
plt.tight_layout()
plt.savefig("images/revenue_by_category.png", dpi=140)
plt.close()

plt.figure(figsize=(8, 5))
plt.barh(state_series.index[::-1], state_series.values[::-1], color="#FF9900")
plt.title("Top 10 States by Revenue", fontsize=13, fontweight="bold")
plt.xlabel("Revenue (₹)")
plt.tight_layout()
plt.savefig("images/top_states.png", dpi=140)
plt.close()

plt.figure(figsize=(6, 6))
plt.pie(channel_series.values, labels=channel_series.index, autopct="%1.1f%%",
        colors=COLORS, startangle=90)
plt.title("Sales Channel Distribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("images/sales_channel_distribution.png", dpi=140)
plt.close()

print("\nCharts saved to /images")
print("Dashboard data saved to /dashboard/dashboard_data.json")
