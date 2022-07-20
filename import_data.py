import openpyxl
import pandas as pd

def load_data():
    # df = pd.read_excel('data/delivery_data_cleaned.xlsx', engine='openpyxl')
    # df.to_csv('data/delivery_data.csv', index=False)
    df_csv = pd.read_csv('data/delivery_data.csv')
    return df_csv