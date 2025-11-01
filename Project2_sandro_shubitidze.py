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


def data_basic_info(dataframe: pd.DataFrame, data_title:str) -> None:
    
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

def data_statistial_summary(dataframe:pd.DataFrame, data_title:str) -> None:
    print(f"\n --- {data_title.upper()} DATA STATISTICAL ANALYSIS --- \n")
    
    # Numerical columns
    print(" --- Numerical Columns Summary:\n")
    num_desc = dataframe.describe().T 
    num_desc['missing'] = dataframe.isnull().sum()
    num_desc['unique'] = dataframe.nunique()
    print(num_desc.to_string())
    print("\n")

    print(" --- Categorical Columns Summary:\n")
    cat_desc = dataframe.describe(include='object').T
    cat_desc['missing'] = dataframe.isnull().sum()
    cat_desc['unique'] = dataframe.nunique()
    print(cat_desc.to_string())
    print("\n")

    print(" --- First 5 Rows:\n")
    print(dataframe.head().to_string())
    print("\n --- Last 5 Rows:\n")
    print(dataframe.tail().to_string())

def main():
    # verify_data_loading()
    # data_basic_info(customers_df, 'CUSTOMERS')
    # data_basic_info(products_df, 'PRODUCTS')
    # data_basic_info(transactions_df, 'TRANSACTION')
    data_statistial_summary(customers_df, "CUSTOMERS")

if __name__ == "__main__":
    main()
