import pandas as pd
import requests
import sqlite3

url='https://open.er-api.com/v6/latest/USD'

def extract():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def transform(raw_data):
    rates = raw_data['rates']
    df = pd.DataFrame(list(rates.items()), columns=['currency', 'rate'])
    return(df)

def load(df):
    conn = sqlite3.connect('currency.db')
    df.to_sql('currency_rates', con=conn, if_exists='replace', index=False)
    conn.close()

data = extract()
transformed_data = transform(data)
load(transformed_data)

conn= sqlite3.connect('currency.db')
cursor = conn.cursor()
cursor.execute('select * from currency_rates limit 5')
print(cursor.fetchall())
conn.close()