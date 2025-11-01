import calendar
import pandas as pd

customers_df = pd.read_csv("data/original/customers.csv")
products_df = pd.read_csv("data/original/products.csv")
transactions_df = pd.read_csv("data/original/transactions.csv")


def verify_data_loading() -> None:
    print(" --- CUSTOMERS DATA --- ")
    print("\n")
    print(customers_df.head())
    print("\n")
    print(" -----------------------------------")
    print("\n")
    print(" --- PRODUCTS DATA --- ")
    print("\n")
    print(products_df.head())
    print("\n")
    print(" -----------------------------------")
    print("\n")
    print(" --- TRANSACTIONS DATA --- ")
    print("\n")
    print(transactions_df.head())


def data_basic_info(dataframe: pd.DataFrame, data_title: str) -> None:

    print(f" --- {data_title} DATA BASIC INFO --- ")
    print("\n")
    print(" --- FIRST 5 ROW --- ")
    print(dataframe.head())
    print("\n")
    print(" --- LAST 5 ROW --- ")
    print(dataframe.tail())
    print("\n")
    print(f" --- {data_title} DATA SHAPE --- ")
    print(f" Number of Rows: {dataframe.shape[0]}")
    print(f" Number of Columns: {dataframe.shape[1]}")
    print("\n")
    print(f" --- {data_title} DATA COLUMNS AND DATA TYPES --- ")
    print(f" Columns: {dataframe.info}")
    print("\n")
    print(f" --- {data_title} DATA MEMORY USAGE  --- ")
    print(f"{dataframe.memory_usage(deep=True)}")
    print(f"Total Memory: {dataframe.memory_usage(deep=True).sum()}")


def data_statistial_summary(dataframe: pd.DataFrame, data_title: str) -> None:
    print(f"\n --- {data_title.upper()} DATA STATISTICAL ANALYSIS --- \n")

    # Numerical columns
    print(" --- Numerical Columns Summary:\n")
    num_desc = dataframe.describe().T
    num_desc["missing"] = dataframe.isnull().sum()
    num_desc["unique"] = dataframe.nunique()
    print(num_desc.to_string())
    print("\n")

    print(" --- Categorical Columns Summary:\n")
    cat_desc = dataframe.describe(include="object").T
    cat_desc["missing"] = dataframe.isnull().sum()
    cat_desc["unique"] = dataframe.nunique()
    print(cat_desc.to_string())
    print("\n")

    print(" --- First 5 Rows:\n")
    print(dataframe.head().to_string())
    print("\n --- Last 5 Rows:\n")
    print(dataframe.tail().to_string())


def data_quality(dataframe: pd.DataFrame, data_title: str) -> None:
    print(dataframe.isnull().sum())
    print((dataframe.isnull().mean() * 100).round(2))
    print(dataframe.duplicated().sum())

    for col in dataframe.select_dtypes(include=["int64", "float64"]).columns:
        print(f"--- {col} ---")
        print(dataframe[col].describe())
        q1 = dataframe[col].quantile(0.25)
        q3 = dataframe[col].quantile(0.75)
        iqr = q3 - q1
        outliers = dataframe[
            (dataframe[col] < q1 - 1.5 * iqr) | (dataframe[col] > q3 + 1.5 * iqr)
        ]
        print(f"Outliers in {col}: {len(outliers)}\n")

    for col in dataframe.select_dtypes(include="object").columns:
        print(f"--- {col} unique values ---")
        print(dataframe[col].value_counts())
        print()


def customer_analysis(dataframe: pd.DataFrame, data_title: str = "CUSTOMER") -> None:
    country_map = {"US": "United States", "USA": "United States"}

    dataframe["country"] = dataframe["country"].replace(country_map)

    dataframe["age"] = dataframe["age"].str.extract("(\d+)")
    dataframe["age"] = pd.to_numeric(dataframe["age"])
    dataframe = dataframe[(dataframe["age"] > 0) & (dataframe["age"] < 150)]

    dataframe["registration_date"] = pd.to_datetime(
        dataframe["registration_date"], errors="coerce"
    )
    dataframe["registration_month"] = dataframe["registration_date"].dt.month

    customer_per_country = dataframe["country"].value_counts(ascending=True)
    age_stats = dataframe["age"].agg(["min", "max", "mean", "median"])
    registrations_per_month = (
        dataframe["registration_month"].value_counts().sort_index()
    )
    registrations_dict = registrations_per_month.to_dict()
    registrations_dict_str = {
        calendar.month_name[k]: v for k, v in registrations_dict.items()
    }

    print("\n --- CUSTOMER ANALYSIS \n")
    print(f"--- Customers per country ---\n{customer_per_country}")
    print(f"\n--- Customers age distribution ---\n{age_stats.round(2)}")
    print("\n--- Customer registration per month ---\n")
    for key, value in registrations_dict_str.items():
        print(key, ":", value)


def product_analysis(products_df: pd.DataFrame):
   

    print("--- PRODUCTS PER CATEGORY ---")
    products_per_category = products_df["category"].value_counts()
    print(products_per_category, "\n")

    print("--- AVERAGE PRICE PER CATEGORY ---")
    avg_price_per_category = products_df.groupby("category")["price"].mean()
    print(avg_price_per_category, "\n")

    print("--- OUT OF STOCK PRODUCTS ---")
    out_of_stock = products_df[products_df["stock"] == 0]
    if not out_of_stock.empty:
        print(out_of_stock[["product_id", "product_name", "category", "stock"]])
    else:
        print("All products are in stock.\n")

def transaction_analysis(transactions_df: pd.DataFrame):
    
    print("--- TRANSACTIONS PER PAYMENT METHOD ---")
    transactions_per_payment = transactions_df['payment_method'].value_counts()
    print(transactions_per_payment, "\n")
    
    print("--- MOST POPULAR PRODUCT ---")
    most_popular_product_id = transactions_df['product_id'].value_counts().idxmax()
    most_popular_count = transactions_df['product_id'].value_counts().max()
    print(f"Product ID: {most_popular_product_id}, Transactions: {most_popular_count}\n")
    
    print("--- CUSTOMER WITH MOST PURCHASES ---")
    top_customer_id = transactions_df['customer_id'].value_counts().idxmax()
    top_customer_count = transactions_df['customer_id'].value_counts().max()
    print(f"Customer ID: {top_customer_id}, Purchases: {top_customer_count}\n")
    
def main():
    # verify_data_loading()
    # data_basic_info(customers_df, 'CUSTOMERS')
    # data_basic_info(products_df, 'PRODUCTS')
    # data_basic_info(transactions_df, 'TRANSACTION')
    # data_statistial_summary(customers_df, "CUSTOMERS")
    # data_statistial_summary(products_df, "PRODUCTS")
    # data_statistial_summary(transactions_df, "TRANSACTION")
    # data_quality(customers_df, 'CUSTOMERS')
    # data_quality(customers_df, 'PRODUCTS')
    # data_quality(customers_df, 'TRANSACTION')
    customer_analysis(customers_df)
    product_analysis(products_df)
    transaction_analysis(transactions_df)


if __name__ == "__main__":
    main()
