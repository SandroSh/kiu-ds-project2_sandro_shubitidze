# Task 1 

This script loads and analyzes three datasets: **customers**, **products**, and **transactions**.

It can:

- Show first and last rows of each dataset  
- Display shape, columns, data types, and memory usage  
- Provide summary statistics for numerical and categorical data  
- Check for missing values, duplicates, and outliers  
- Analyze customers: age, country, registration months  
- Analyze products: category, price, and out-of-stock items  
- Analyze transactions: payment methods, popular products, top customers  

---

## Usage

uncomment functions in main


# Task 2

This project cleans and prepares the datasets for analysis. It handles missing values, duplicates, outliers, inconsistent data types, and standardizes text. Cleaned datasets are saved in `data/cleaned/`.

---

## Features

### Customers (`customers.csv`)
- Clean emails, drop missing, remove duplicates  
- Convert `age` to integer, fix invalid values  
- Standardize country names (`US`/`USA` → `United States`)  

### Products (`products.csv`)
- Clean names and categories, remove duplicates  
- Fill missing prices, fix negatives, cap stock at 500  
- Ensure numeric types for price and stock  

### Transactions (`transactions.csv`)
- Clean `payment_method`, remove duplicates  
- Fill missing `quantity`, convert to numeric  
- Convert `transaction_date` to datetime, remove future dates  

---

## Usage
just uncomment function executions in main



#  Task 3
This Python module performs **data loading, cleaning, feature engineering, and analysis** on a retail dataset containing customers, products, and transactions.


## Features

## Features
- Merge transactions with customer and product data
- Financial: total, discount, final amount
- Temporal: month, day of week, age at purchase
- Categorical: customer segment, age group, weekend flag

## Analysis
- Revenue by category, month, country, payment method
- Customer behavior: top customers, spending by age, popular category, weekend vs weekday
- Product performance: top products by revenue/quantity, category with highest avg transaction, slow movers

## Usage

```python
uncomment code below of file