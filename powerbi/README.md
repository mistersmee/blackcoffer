# Task 3: Create a dashboard in PowerBI using sample dataset, use DAX as well.

## Introduction

Microsoft PowerBI is an extemely powerful Business Intelligence software, that allows you to create interactive dashboards and reports from a wide variety of data sources. 
It is one of the industry standard applications as it allows you to create very detailed and insightful dashboards.
It also has a built-in DAX (Data Analysis Expressions) engine that allows you to write specific queries to get detailed data based upon the dataset that is being used.

## Information about the Dataset

The dataset that I used is a sample dataset of sales of products in supermarket chain. It has about 1000 entries, across three branches in three different cities.

The fields in the dataset are:

- Invoice ID
- Branch
- City
- Customer Type
- Gender
- Product Line
- Unit Price
- Quantity
- Tax 5%
- Total
- Date
- Time
- Payment Method
- COGS (Cost of Goods Sold)
- Gross Margin Percentage
- Gross Income
- Rating

## DAX queries used:

PowerBI allows you to create DAX expressions in two ways: 
1) As calculated measures
2) As standalone queries in the DAX query view


The calculated measures I created using DAX expressions are:
- Average Gross Margin Percentage: `AVERAGE('supermarket'[Gross Margin Percentage])`
- Average Unit Price: `AVERAGE('supermarket'[Unit Price])`
- Customer Count by Type: `CALCULATE(DISTINCTCOUNT('supermarket'[Invoice ID]), ALLEXCEPT('supermarket', 'supermarket'[Customer Type]))`
- Monthly Sales: `CALCULATE(SUM('supermarket'[Total]), YEAR('supermarket'[Date]) = YEAR(TODAY()), MONTH('supermarket'[Date]) = MONTH(TODAY()))`
- Sales per Customer: `AVERAGEX(VALUES('supermarket'[Invoice ID]), CALCULATE(SUM('supermarket'[Total])))`
- Total COGS: `SUM('supermarket'[COGS])`
- Total Gross Margin: `SUM('supermarket'[Gross Income])`
- Total Quantity Sold: `SUM('supermarket'[Quantity])`
- Total Sales: `SUM('supermarket'[Total])`
- Total Tax: `SUM('supermarket'[Tax 5%])`
- YoY Growth: `(SUM('supermarket'[Total]) - CALCULATE(SUM('supermarket'[Total]), SAMEPERIODLASTYEAR('supermarket'[Date]))) / CALCULATE(SUM('supermarket'[Total]), SAMEPERIODLASTYEAR('supermarket'[Date]))`


The queries I created in the DAX query view are similar to the ones listed above, but they follow a different syntax like so:


Total Sales:
```DAX
EVALUATE 
SUMMARIZE(
    'supermarket',
    "Total Sales", SUM('supermarket'[Total])
)
```

## Visualisations Created

I created the following visualisations in the dashboard:

- Scorecards (KPI metrics): Sum of Quantity, Sum of Total Sales, Average of Unit Price, Highest Sales by City
- Visualisations using charts: Sum of Quantity by Product Line, Sum of Quantity by Date, Sum of Quantity by City, Average of Rating by Product Line
- Filters: By City, By Date, By Product Line

## Work Done By:

Aseem Athale

athaleaseem@gmail.com
