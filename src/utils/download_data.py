import json 
import psycopg
import pandas as pd

with open('config/database.json') as f:
   db_info = json.load(f)

def connect_db(in_sample=True):
    with psycopg.connect(
      host=db_info['host'],
      port=db_info['port'],
      dbname=db_info['database'],
      user=db_info['user'],
      password=db_info['password']) as conn:
    # Open a cursor to perform database operations
      with conn.cursor() as cur:

         if in_sample:
            # Execute a query
            cur.execute("""
                  SELECT m.datetime, m.tickersymbol, m.price, v.quantity
                  FROM "quote"."matched" m
                  LEFT JOIN "quote"."total" v
                  ON m.tickersymbol = v.tickersymbol
                  and m.datetime =  v.datetime
                  where m.datetime between '2023-1-1' and '2024-12-31'
                  and m.tickersymbol LIKE 'VN30F23%' OR m.tickersymbol LIKE 'VN30F24%'
            """)

            # Use fetchall() to get all the data of the query.
            # Note: fetchall() can be costly and inefficient.
            # Other efficient ways have been discussed extensively on the Internet. Or you can ask ChatGPT ;)
            in_sample_data = cur.fetchall()

            # Print the total number of ticks of that day
            print(f'Total number of tick: {len(in_sample_data)}')
            save_data(in_sample_data, 'database/indata.csv')
         else:
            cur.execute("""
                  SELECT m.datetime, m.tickersymbol, m.price, v.quantity
                  FROM "quote"."matched" m
                  LEFT JOIN "quote"."total" v
                  ON m.tickersymbol = v.tickersymbol
                  and m.datetime =  v.datetime
                  where m.datetime between '2021-1-1' and '2022-12-31'
                  and m.tickersymbol LIKE 'VN30F21%' OR m.tickersymbol LIKE 'VN30F22%'
            """)
            out_sample_data = cur.fetchall()
            print(f'Total number of tick: {len(out_sample_data)}')
            save_data(out_sample_data, 'database/outdata.csv')
    

def save_data(data, file_path):
   df = pd.DataFrame(data, columns=['datetime', 'tickersymbol', 'price', 'quantity'])
   df['datetime'] = pd.to_datetime(df['datetime'])

   df.to_csv(file_path, index=False)
   print(f"Data saved to {file_path}")

def load_data(file_path):
   in_sample_data = pd.read_csv(file_path)
   df = pd.DataFrame(in_sample_data, columns=['datetime', 'tickersymbol', 'price', 'quantity'])
   df['datetime'] = pd.to_datetime(df['datetime'])

   df.set_index('datetime', inplace=True)
   # print(df.dtypes)

   df['price'] = pd.to_numeric(df['price'], errors='coerce')

   ohlc = df['price'].resample('D').ohlc()
   ohlc['volume'] = df['quantity'].resample('D').sum()
   ohlc = ohlc.dropna()

# print(ohlc.head())
   return ohlc


# in_sample_data = connect_db(True)
