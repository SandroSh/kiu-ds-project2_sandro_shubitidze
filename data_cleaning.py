import pandas as pd
from Project2_sandro_shubitidze import customers_df, products_df, transactions_df
import os



def check_customers_data_quality(customers_df: pd.DataFrame):
    """
    Check for data quality issues in customers.csv:
    - Missing values
    - Duplicate rows
    - Inconsistent data types
    - Inconsistent country names (like USA, US, United States)
    """
    customers_df["age"] = (
        customers_df["age"]
        .astype(str)
        .str.extract("(\d+)")[0]  # keep only digits
        .astype(float)  # convert to float
    )

    print("--- MISSING VALUES PER COLUMN ---")
    print(customers_df.isnull().sum(), "\n")

    print("--- DUPLICATE ROWS ---")
    duplicate_count = customers_df.duplicated().sum()
    print(f"Total duplicate rows: {duplicate_count}\n")

    print("--- DATA TYPES ---")
    print(customers_df.dtypes, "\n")

    print("--- INCONSISTENT AGE VALUES ---")
    invalid_ages = customers_df[(customers_df["age"] < 0) | (customers_df["age"] > 120)]
    if invalid_ages.empty:
        print("All ages are within a valid range.\n")
    else:
        print("Invalid age entries:\n", invalid_ages, "\n")

    print("--- INCONSISTENT COUNTRY NAMES ---")
    country_counts = customers_df["country"].value_counts()
    print(country_counts, "\n")

    # Normalize inconsistent country names
    customers_df["country"] = customers_df["country"].replace(
        {"US": "United States", "USA": "United States"}
    )

    print("--- FIXED COUNTRY NAMES ---")
    print(customers_df["country"].value_counts(), "\n")

def check_products_data_quality(products_df: pd.DataFrame):
    """
    Check data quality issues in products.csv:
    - Missing values in price
    - Negative or zero prices (data entry errors)
    - Unrealistic stock values
    - Whitespace around product names
    - Inconsistent category naming (mixed case)
    """

    print("--- MISSING VALUES PER COLUMN ---")
    print(products_df.isnull().sum(), "\n")

    print("--- CHECKING PRICE COLUMN ---")

    products_df["price"] = pd.to_numeric(products_df["price"], errors="coerce")
    missing_price = products_df["price"].isnull().sum()
    print(f"Missing prices: {missing_price}")

    negative_prices = products_df[products_df["price"] < 0]
    if negative_prices.empty:
        print("No negative prices found.\n")
    else:
        print("Negative price entries:\n", negative_prices, "\n")

    print("--- CHECKING STOCK VALUES ---")
    unrealistic_stock = products_df[
        (products_df["stock"] < 0) | (products_df["stock"] > 10000)
    ]
    if unrealistic_stock.empty:
        print("Stock values are within reasonable range.\n")
    else:
        print("Unrealistic stock values:\n", unrealistic_stock, "\n")

    print("--- FIXING WHITESPACE IN PRODUCT NAMES ---")
    products_df["product_name"] = products_df["product_name"].str.strip()
    print("Whitespace removed from product names.\n")

    print("--- INCONSISTENT CATEGORY NAMES ---")
    print("Before normalization:")
    print(products_df["category"].value_counts(), "\n")

    # Normalize category names (remove spaces + make title case)
    products_df["category"] = products_df["category"].str.strip().str.title()

    print("After normalization:")
    print(products_df["category"].value_counts(), "\n")

    print("--- DATA QUALITY CHECK COMPLETE ---")

def check_transactions_data_quality(transactions_df: pd.DataFrame, customers_df: pd.DataFrame):
    """
    Check data quality issues in transactions.csv:
    - Missing quantities
    - Duplicate transaction IDs
    - Invalid customer_id references (not found in customers.csv)
    - Future transaction dates
    - Inconsistent payment_method naming
    """

    print("--- MISSING VALUES PER COLUMN ---")
    print(transactions_df.isnull().sum(), "\n")

    print("--- CHECKING QUANTITY COLUMN ---")
    missing_quantity = transactions_df["quantity"].isnull().sum()
    print(f"Missing quantity entries: {missing_quantity}")

    invalid_quantities = transactions_df[transactions_df["quantity"] <= 0]
    if invalid_quantities.empty:
        print("No invalid (zero or negative) quantities found.\n")
    else:
        print("Invalid quantity rows:\n", invalid_quantities, "\n")

    print("--- CHECKING DUPLICATE TRANSACTION IDs ---")
    duplicate_ids = transactions_df["transaction_id"].duplicated().sum()
    print(f"Duplicate transaction IDs: {duplicate_ids}\n")

    print("--- CHECKING INVALID CUSTOMER REFERENCES ---")
    invalid_customers = ~transactions_df["customer_id"].isin(
        customers_df["customer_id"]
    )
    invalid_refs = transactions_df[invalid_customers]
    if invalid_refs.empty:
        print("All customer_id references are valid.\n")
    else:
        print("Invalid customer_id references found:\n", invalid_refs, "\n")

    print("--- CHECKING FUTURE DATES ---")
    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"], errors="coerce"
    )
    future_dates = transactions_df[
        transactions_df["transaction_date"] > pd.Timestamp.today()
    ]
    if future_dates.empty:
        print("No future transaction dates found.\n")
    else:
        print("Future transactions detected:\n", future_dates, "\n")

    print("--- CHECKING PAYMENT METHOD CONSISTENCY ---")
    print("Before normalization:")
    print(transactions_df["payment_method"].value_counts(), "\n")

    # Normalize inconsistent payment method names
    transactions_df["payment_method"] = (
        transactions_df["payment_method"].str.strip().str.title()
    )

    print("After normalization:")
    print(transactions_df["payment_method"].value_counts(), "\n")

    print("--- DATA QUALITY CHECK COMPLETE ---")

def clean_customers(customers_df: pd.DataFrame):

    df = customers_df.copy()
    report = {
        "initial_rows": len(df),
        "dropped_missing_email": 0,
        "duplicate_rows_found": 0,
        "duplicate_rows_removed": 0,
        "age_non_numeric_before": 0,
        "age_invalid_set_na": 0,
        "registration_date_coerced": 0,
        "final_rows": None,
    }

    # ----------  Strip whitespace ----------
    text_cols = ["name", "email", "country"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # ----------  Lowercase email & drop missing ----------
    df["email"] = df["email"].replace(["", "None", "nan"], pd.NA).str.lower()
    missing_before = df["email"].isna().sum()
    df = df[df["email"].notna()].copy()
    report["dropped_missing_email"] = int(missing_before)

    # ----------  Remove duplicates ----------
    dup_count = df.duplicated(keep="first").sum()
    df = df.drop_duplicates(keep="first").copy()
    report["duplicate_rows_found"] = int(dup_count)
    report["duplicate_rows_removed"] = int(dup_count)

    # ---------- Fix age column ----------
    # Extract digits, convert to numeric, set invalid to NA
    report["age_non_numeric_before"] = int(
        (~df["age"].astype(str).str.contains(r"\d")).sum()
    )
    df["age"] = df["age"].astype(str).str.extract(r"(\d+)").astype(float)
    invalid_age_mask = (df["age"] <= 0) | (df["age"] > 120)
    report["age_invalid_set_na"] = int(invalid_age_mask.sum())
    df.loc[invalid_age_mask, "age"] = pd.NA
    df["age"] = df["age"].astype("Int64")

    # ---------- Fix registration_date ----------
    before_valid = df["registration_date"].notna().sum()
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    after_valid = df["registration_date"].notna().sum()
    report["registration_date_coerced"] = int(before_valid - after_valid)

    # ---------- Standardize country names ----------
    df["country"] = df["country"].astype(str).str.strip()
    country_map = {
        "US": "United States",
        "Us": "United States",
        "USA": "United States",
        "Usa": "United States",
        "U.S.": "United States",
        "U.S.A.": "United States",
    }
    df["country"] = df["country"].replace(country_map)

    # ---------- Final report ----------
    report["final_rows"] = len(df)

    print("--- CUSTOMERS DATA CLEANING REPORT ---")
    print(f"Initial rows: {report['initial_rows']}")
    print(f"Dropped rows with missing email: {report['dropped_missing_email']}")
    print(f"Duplicate rows removed: {report['duplicate_rows_removed']}")
    print(f"Invalid ages set to NA: {report['age_invalid_set_na']}")
    print(
        f"Invalid registration dates coerced to NaT: {report['registration_date_coerced']}"
    )
    print(f"Final rows: {report['final_rows']}")
    print("--------------------------------------\n")

    return df.reset_index(drop=True), report

def clean_products(products_df: pd.DataFrame):

    df = products_df.copy()
    report = {
        "initial_rows": len(df),
        "missing_price_filled": 0,
        "duplicates_removed": 0,
        "negative_prices_fixed": 0,
        "unrealistic_stock_capped": 0,
        "final_rows": None,
    }

    # ----------  Strip whitespace ----------
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip().str.title()

    # ---------- Handle missing values ----------
    # Fill missing price with median of same category
    missing_before = df["price"].isna().sum()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["price"] = df.groupby("category")["price"].transform(
        lambda x: x.fillna(x.median())
    )
    report["missing_price_filled"] = int(missing_before)

    # ---------- Remove duplicate rows ----------
    dup_count = df.duplicated(keep="first").sum()
    df = df.drop_duplicates(keep="first").copy()
    report["duplicates_removed"] = int(dup_count)

    # ---------- Fix data types ----------
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)

    # ---------- Handle invalid values ----------
    # Fix negative prices
    neg_price_mask = df["price"] < 0
    report["negative_prices_fixed"] = int(neg_price_mask.sum())
    df.loc[neg_price_mask, "price"] = df["price"].median()

    # Cap unrealistic stock values at 500
    unrealistic_mask = df["stock"] > 500
    report["unrealistic_stock_capped"] = int(unrealistic_mask.sum())
    df.loc[unrealistic_mask, "stock"] = 500

    # ---------- Final report ----------
    report["final_rows"] = len(df)

    print("--- PRODUCTS DATA CLEANING REPORT ---")
    print(f"Initial rows: {report['initial_rows']}")
    print(f"Missing prices filled: {report['missing_price_filled']}")
    print(f"Duplicate rows removed: {report['duplicates_removed']}")
    print(f"Negative prices fixed: {report['negative_prices_fixed']}")
    print(f"Unrealistic stock capped (at 500): {report['unrealistic_stock_capped']}")
    print(f"Final rows: {report['final_rows']}")
    print("--------------------------------------\n")

    return df.reset_index(drop=True), report

def clean_transactions(transactions_df: pd.DataFrame):

    df = transactions_df.copy()
    report = {
        "initial_rows": len(df),
        "missing_quantity_filled": 0,
        "duplicates_removed": 0,
        "future_dates_removed": 0,
        "final_rows": None,
    }

    # ---------- Strip whitespace  ----------
    df["payment_method"] = df["payment_method"].astype(str).str.strip().str.title()

    # ----------  Fix data types ----------
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    # ---------- Handle missing quantities ----------
    missing_before = df["quantity"].isna().sum()
    if missing_before > 0:
        mode_quantity = (
            df["quantity"].mode()[0] if not df["quantity"].mode().empty else 1
        )
        df["quantity"] = df["quantity"].fillna(mode_quantity)
    report["missing_quantity_filled"] = int(missing_before)

    # ---------- Remove duplicates ----------
    dup_count = df.duplicated(keep="first").sum()
    df = df.drop_duplicates(keep="first").copy()
    report["duplicates_removed"] = int(dup_count)


    # ---------- Final report ----------
    report["final_rows"] = len(df)

    print("--- TRANSACTIONS DATA CLEANING REPORT ---")
    print(f"Initial rows: {report['initial_rows']}")
    print(f"Missing quantities filled: {report['missing_quantity_filled']}")
    print(f"Duplicate rows removed: {report['duplicates_removed']}")
    print(f"Future dates removed: {report['future_dates_removed']}")
    print(f"Final rows: {report['final_rows']}")
    print("------------------------------------------\n")
    
    return df.reset_index(drop=True), report


def save_cleaned_df(df: pd.DataFrame, filename: str):

    output_folder = "data/cleaned"
    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(output_folder, filename)

    df.to_csv(file_path, index=False)
    print(f"Saved cleaned data to {file_path}")
    
def customer_report():
    cleaned_customers_df, report = clean_customers(customers_df)

    customer_report = pd.DataFrame(
        {
            "Metric": [
                "Original row count",
                "Cleaned row count",
                "Rows dropped (missing email)",
                "Duplicate rows removed",
                "Invalid ages set to NA",
                "Invalid registration_dates coerced",
                "Data types corrected",
            ],
            "Count": [
                report["initial_rows"],
                report["final_rows"],
                report["dropped_missing_email"],
                report["duplicate_rows_removed"],
                report["age_invalid_set_na"],
                report["registration_date_coerced"],
                "age -> Int64, registration_date -> datetime",
            ],
        }
    )

    missing_values_after = cleaned_customers_df.isna().sum()
    duplicates_after = cleaned_customers_df.duplicated().sum()
    dtypes_after = cleaned_customers_df.dtypes

    print("\n--- CUSTOMER CLEANING REPORT ---")
    print(customer_report)
    print("\n--- MISSING VALUES AFTER CLEANING ---")
    print(missing_values_after)
    print("\n--- DUPLICATES AFTER CLEANING ---")
    print(duplicates_after)
    print("\n--- DATA TYPES AFTER CLEANING ---")
    print(dtypes_after)
    print("---------------------------------\n")

    save_cleaned_df(cleaned_customers_df, 'customers.csv')
def product_report():
    cleaned_products_df, report = clean_products(products_df)

    product_report_df = pd.DataFrame(
        {
            "Metric": [
                "Original row count",
                "Cleaned row count",
                "Missing prices filled",
                "Duplicate rows removed",
                "Negative prices fixed",
                "Unrealistic stock capped",
                "Data types corrected",
            ],
            "Count": [
                report["initial_rows"],
                report["final_rows"],
                report["missing_price_filled"],
                report["duplicates_removed"],
                report["negative_prices_fixed"],
                report["unrealistic_stock_capped"],
                "price -> numeric, stock -> int",
            ],
        }
    )

    missing_values_after = cleaned_products_df.isna().sum()
    duplicates_after = cleaned_products_df.duplicated().sum()
    dtypes_after = cleaned_products_df.dtypes

    print("\n--- PRODUCTS CLEANING REPORT ---")
    print(product_report_df)
    print("\n--- MISSING VALUES AFTER CLEANING ---")
    print(missing_values_after)
    print("\n--- DUPLICATES AFTER CLEANING ---")
    print(duplicates_after)
    print("\n--- DATA TYPES AFTER CLEANING ---")
    print(dtypes_after)
    print("---------------------------------\n")

    save_cleaned_df(cleaned_products_df, 'products_clean.csv')
def transactions_report():
    cleaned_transactions_df, report = clean_transactions(transactions_df)

    transactions_report_df = pd.DataFrame(
        {
            "Metric": [
                "Original row count",
                "Cleaned row count",
                "Missing quantities filled",
                "Duplicate rows removed",
                "Future dates removed",
                "Data types corrected",
            ],
            "Count": [
                report["initial_rows"],
                report["final_rows"],
                report["missing_quantity_filled"],
                report["duplicates_removed"],
                report["future_dates_removed"],
                "quantity -> numeric, transaction_date -> datetime",
            ],
        }
    )

    missing_values_after = cleaned_transactions_df.isna().sum()
    duplicates_after = cleaned_transactions_df.duplicated().sum()
    dtypes_after = cleaned_transactions_df.dtypes

    print("\n--- TRANSACTIONS CLEANING REPORT ---")
    print(transactions_report_df)
    print("\n--- MISSING VALUES AFTER CLEANING ---")
    print(missing_values_after)
    print("\n--- DUPLICATES AFTER CLEANING ---")
    print(duplicates_after)
    print("\n--- DATA TYPES AFTER CLEANING ---")
    print(dtypes_after)
    print("---------------------------------\n")

    save_cleaned_df(cleaned_transactions_df, 'transactions_clean.csv')

def main():
    # check_customers_data_quality(customers_df)
    # check_products_data_quality(products_df)
    # check_transactions_data_quality(transactions_df, customers_df)
    # customer_report()
    # product_report()
    # transactions_report()
    pass


if __name__ == "__main__":
    main()
