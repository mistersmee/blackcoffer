# Task 4: Create a dashboard in Google Data Studio using sample dataset, Incorporate Data computations

## Introduction

Google Data Studio is a platform that allows you to create interactive dashboards and reports that allow users to perform Business Intelligence tasks easily and using the cloud. No desktop application is required to perform Business Intelligence tasks unlike other applications like Microsoft PowerBI or Tableau.

## Information about the dataset

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


# Data Computations created

In order to provide useful insights, I created custom data computations based on the existing fields. The data computations I created are:

- Net Sales: `Total / 1.05`
- Average Customer Rating: `AVG(Rating)`
- Average Transactional Value: `AVG(Total)`
- Gross Profit: `SUM(gross income)`
- Gross Profit Margin: `( Gross Profit / SUM(Total) ) * 100`
- Total Revenue: `SUM(Total)`
- Transaction Count: `COUNT(Invoice ID)`

# Visualisations Created

The dashboard I created spans 4 pages, each of the pages are as follows:

- Executive Summary
- Sales Analysis
- Customer Insights
- Other Metrics

Executive summary contains all of the key metrics that one can view at a glance and get an understanding of the basic data contained in the dataset, like Total Revenue, Total Units Sold, Average Transactional Value, Gross Profit, Average Customer Rating and Transaction Count. It also contains visualisations of Revenue by Payment method and sales by branch.

Sales Analysis contains visualisations of Sales by Product Line, Top 5 Selling Products, and Product Line Statistics.

Customer Insights contains visualisations of Customer type Distribution, Gender Sales Split and Average Rating by Customer Type.

And finally Other Metrics contain visualisations of Monthly Revenue Trend, City-wise Revenue and Branch Comparison.

# Work Done by:

Aseem Athale

athaleaseem@gmail.com
