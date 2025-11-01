import pandas as pd

customers_df = pd.read_csv('data/original/customers.csv')
products_df = pd.read_csv('data/original/products.csv')
transactions_df = pd.read_csv('data/original/transactions.csv')

def verify_data_loading():
    print(' === CUSTOMERS DATA === ')
    print('\n')
    print(customers_df.head())
    print('\n')
    print(' ================================== ')
    print('\n')
    print(' === PRODUCTS DATA === ')
    print('\n')
    print(products_df.head())
    print('\n')
    print(' ================================== ')
    print('\n')
    print(' === TRANSACTIONS DATA === ')
    print('\n')
    print(transactions_df.head())
    
    


def main():
    verify_data_loading()

if __name__ == '__main__':
    main()