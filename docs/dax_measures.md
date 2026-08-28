# Power BI — DAX Measures Reference

This project ships a fully working **HTML/Chart.js dashboard** (`dashboard/index.html`) so the
KPIs are viewable without installing anything. If you also want the actual **Power BI Desktop
(.pbix)** file referenced in the project description, open Power BI Desktop, import
`data/amazon_sales_data.csv`, and paste in the DAX measures below — this recreates all 15+ KPIs
shown on the dashboard in native Power BI visuals.

> Power BI `.pbix` files are a proprietary binary format and can't be generated from a script,
> so they're rebuilt locally in Power BI Desktop using this file as the data source.

## 1. Load the data
`Get Data → Text/CSV → data/amazon_sales_data.csv → Load`

Set data types: `Order_Date` → Date, `Net_Sales`/`Profit`/`Cost`/`Discount_Amount` → Decimal,
`Quantity`/`Is_Returned`/`Customer_Rating` → Whole Number.

## 2. Core measures

```DAX
Total Revenue = SUM(amazon_sales_data[Net_Sales])

Total Profit = SUM(amazon_sales_data[Profit])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(amazon_sales_data[Order_ID])

Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Total Units Sold = SUM(amazon_sales_data[Quantity])

Unique Customers = DISTINCTCOUNT(amazon_sales_data[Customer_ID])

Avg Revenue per Customer = DIVIDE([Total Revenue], [Unique Customers], 0)

Return Rate % = DIVIDE(
    CALCULATE(COUNTROWS(amazon_sales_data), amazon_sales_data[Is_Returned] = 1),
    COUNTROWS(amazon_sales_data), 0
)

Avg Customer Rating = AVERAGE(amazon_sales_data[Customer_Rating])

Avg Discount % = AVERAGE(amazon_sales_data[Discount_Percent])

Prime Member Revenue Share % = DIVIDE(
    CALCULATE([Total Revenue], amazon_sales_data[Customer_Segment] = "Prime Member"),
    [Total Revenue], 0
)
```

## 3. Time-intelligence measures

```DAX
Revenue YTD = TOTALYTD([Total Revenue], amazon_sales_data[Order_Date])

Revenue PY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(amazon_sales_data[Order_Date]))

Revenue YoY % = DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY], 0)

Revenue MoM % =
VAR CurrM = [Total Revenue]
VAR PrevM = CALCULATE([Total Revenue], DATEADD(amazon_sales_data[Order_Date], -1, MONTH))
RETURN DIVIDE(CurrM - PrevM, PrevM, 0)
```

## 4. Ranking measures (Top N cards)

```DAX
Top Category by Revenue =
CALCULATE(
    VALUES(amazon_sales_data[Category]),
    TOPN(1, VALUES(amazon_sales_data[Category]), [Total Revenue], DESC)
)

Top Product by Revenue =
CALCULATE(
    VALUES(amazon_sales_data[Product_Name]),
    TOPN(1, VALUES(amazon_sales_data[Product_Name]), [Total Revenue], DESC)
)
```

## 5. Suggested visuals (15+ KPI layout)

| Visual | Fields |
|---|---|
| Card | Total Revenue, Total Profit, Profit Margin %, Total Orders, Avg Order Value |
| Card | Unique Customers, Return Rate %, Avg Customer Rating |
| Line chart | Order_Date (month) vs Total Revenue, Total Profit |
| Bar chart | Category vs Total Revenue |
| Bar chart | Product_Name (Top 10) vs Total Revenue |
| Map / Bar | State vs Total Revenue |
| Donut | Sales_Channel vs Total Revenue |
| Donut | Payment_Mode vs Total Orders |
| Donut | Customer_Segment vs Total Revenue |
| Column | Weekday(Order_Date) vs Total Revenue |
| Slicers | Order_Date, Category, State, Sales_Channel, Customer_Segment |

## 6. Publish
`File → Publish → Power BI Service` (or export as `.pbix` from `File → Save As`) once the report
matches the layout above. Rename the file to `Amazon_Sales_Analytics_Dashboard.pbix` and drop it
into a `powerbi/` folder in this repo if you want both the live web build and the native file
side by side.
