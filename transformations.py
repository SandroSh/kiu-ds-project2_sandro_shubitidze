import pandas as pd
from Project2_sandro_shubitidze import customers_df, products_df, transactions_df


import pandas as pd

def create_transaction_view(customers_df, products_df, transactions_df):
    """
    Used left join and transactions as primary table to have all trasnasctions kept
    """

    merged_cust = transactions_df.merge(
        customers_df,
        on="customer_id",
        how="left",
        indicator=True,  
    )

    unmatched_customers = merged_cust["_merge"].value_counts().get("left_only", 0)
    merged_cust.drop(columns="_merge", inplace=True)

    merged_final = merged_cust.merge(
        products_df, on="product_id", how="left", indicator=True
    )

    unmatched_products = merged_final["_merge"].value_counts().get("left_only", 0)
    merged_final.drop(columns="_merge", inplace=True)

    print("unmatched products: ", unmatched_products)
    print("unmatched customers: ", unmatched_customers)

    return cleaned_merged


def add_financial_features(merged_df):
  

    merged_df["price"] = pd.to_numeric(merged_df["price"], errors="coerce")
    merged_df["quantity"] = pd.to_numeric(merged_df["quantity"], errors="coerce")


    merged_df["total_amount"] = merged_df["price"] * merged_df["quantity"]

    merged_df["discount"] = merged_df.apply(
        lambda x: x["total_amount"] * 0.10 if x["quantity"] > 3 else 0, axis=1
    )

    merged_df["final_amount"] = merged_df["total_amount"] - merged_df["discount"]

    

    return merged_df

def add_temporal_features(merged_df):
   
    # Ensure correct datetime type
    merged_df["transaction_date"] = pd.to_datetime(
        merged_df["transaction_date"], errors="coerce"
    )
    merged_df["registration_date"] = pd.to_datetime(
        merged_df["registration_date"], errors="coerce"
    )

    # Extract month and weekday
    merged_df["transaction_month"] = merged_df["transaction_date"].dt.month
    merged_df["transaction_day_of_week"] = merged_df["transaction_date"].dt.day_name()

    merged_df["customer_age_at_purchase"] = (
        merged_df["transaction_date"].dt.year - merged_df["registration_date"].dt.year
    ) + merged_df["age"].fillna(0)

    return merged_df

def add_categorical_features(merged_df):
   
    # Calculate total spending per customer
    total_spending = merged_df.groupby("customer_id")["final_amount"].sum()

    # Map spending to customer_segment
    def spending_segment(value):
        if value > 1000:
            return "High"
        elif 500 <= value <= 1000:
            return "Medium"
        else:
            return "Low"

    spending_map = total_spending.apply(spending_segment)
    merged_df["customer_segment"] = merged_df["customer_id"].map(spending_map)

    # Create age_group column
    def age_group(age):
        if pd.isna(age):
            return "Unknown"
        elif 18 <= age <= 30:
            return "18–30"
        elif 31 <= age <= 45:
            return "31–45"
        elif 46 <= age <= 60:
            return "46–60"
        else:
            return "61+"

    merged_df["age_group"] = merged_df["age"].apply(age_group)

    # Add is_weekend column
    merged_df["is_weekend"] = merged_df["transaction_date"].dt.day_name().isin(
        ["Saturday", "Sunday"]
    )

    return merged_df

def revenue_and_customer_analysis(merged_df):
   
    print("\n--- REVENUE ANALYSIS ---\n")

    # Total revenue by product category
    revenue_by_category = merged_df.groupby("category")["final_amount"].sum().sort_values(ascending=False)
    print("Total Revenue by Product Category:")
    print(revenue_by_category, "\n")

    # Monthly revenue trend
    merged_df["month"] = merged_df["transaction_date"].dt.to_period("M")
    monthly_revenue = merged_df.groupby("month")["final_amount"].sum()
    print("Monthly Revenue Trend:")
    print(monthly_revenue, "\n")

    # Revenue by country (Top 5)
    revenue_by_country = merged_df.groupby("country")["final_amount"].sum().sort_values(ascending=False).head(5)
    print("Top 5 Countries by Revenue:")
    print(revenue_by_country, "\n")

    # Average transaction value by payment method
    avg_transaction_value = merged_df.groupby("payment_method")["final_amount"].mean()
    print("Average Transaction Value by Payment Method:")
    print(avg_transaction_value, "\n")

    print("\n--- CUSTOMER BEHAVIOR ANALYSIS ---\n")

    # Number of purchases per customer (Top 10)
    purchases_per_customer = merged_df["customer_id"].value_counts().head(10)
    print("Top 10 Customers by Purchase Count:")
    print(purchases_per_customer, "\n")

    # Average spending by age group
    avg_spending_by_age_group = merged_df.groupby("age_group")["final_amount"].mean().sort_index()
    print("Average Spending by Age Group:")
    print(avg_spending_by_age_group, "\n")

    # Most popular product category by country
    popular_category_by_country = merged_df.groupby("country")["category"].agg(lambda x: x.value_counts().index[0])
    print("Most Popular Product Category by Country:")
    print(popular_category_by_country, "\n")

    # Weekend vs. Weekday transaction patterns
    weekend_pattern = merged_df.groupby("is_weekend")["final_amount"].agg(["count", "sum", "mean"])
    weekend_pattern.index = weekend_pattern.index.map({True: "Weekend", False: "Weekday"})
    print("Weekend vs Weekday Transaction Patterns:")
    print(weekend_pattern, "\n")

    
    print("\n--- PRODUCT PERFORMANCE ANALYSIS ---\n")

    # Top 10 products by total revenue
    top_products_revenue = (
        merged_df.groupby(["product_id", "product_name"])["final_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print("Top 10 Products by Revenue:")
    print(top_products_revenue, "\n")

    # Top 10 products by quantity sold
    top_products_quantity = (
        merged_df.groupby(["product_id", "product_name"])["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print("Top 10 Products by Quantity Sold:")
    print(top_products_quantity, "\n")

    # Category with highest average transaction value
    avg_value_by_category = merged_df.groupby("category")["final_amount"].mean()
    top_category = avg_value_by_category.idxmax()
    print(f"Category with Highest Average Transaction Value: {top_category}")
    print(avg_value_by_category.sort_values(ascending=False), "\n")
    
    


merged_df = create_transaction_view(customers_df, products_df, transactions_df)

merged_df = add_financial_features(merged_df)
merged_df = add_temporal_features(merged_df)
merged_df = add_categorical_features(merged_df)


revenue_and_customer_analysis(merged_df)