import pandas as pd

def load_data():
    df_csv = pd.read_csv('data/delivery_data.csv')
    return df_csv