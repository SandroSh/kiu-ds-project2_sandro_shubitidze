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
- Strip whitespace and lowercase emails  
- Drop missing emails  
- Remove duplicates  
- Convert `age` to integer, invalid ages → NA  
- Standardize country names (`US`, `USA` → `United States`)  

### Products (`products.csv`)
- Strip whitespace and standardize category names  
- Fill missing prices with median per category  
- Remove duplicates  
- Fix negative prices  
- Cap stock levels at 500  
- Ensure numeric types for price and stock  

### Transactions (`transactions.csv`)
- Strip whitespace and standardize `payment_method`  
- Fill missing `quantity` with mode  
- Remove duplicates  
- Convert `quantity` to numeric and `transaction_date` to datetime  
- Remove future transaction dates  

---

## Usage
just uncomment function executions in main
