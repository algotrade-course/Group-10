import json 
import psycopg
import pandas as pd

with open('config/database.json') as f:
   db_info = json.load(f)

def connect_db(in_sample: bool):
    with psycopg.connect(
      host=db_info['host'],
      port=db_info['port'],
      dbname=db_info['database'],
      user=db_info['user'],
      password=db_info['password']) as conn:
    # Open a cursor to perform database operations
      with conn.cursor() as cur:
         print("Connected to the database")
         if in_sample:
            # Execute a query
            cur.execute("""
                  SELECT m.datetime, m.tickersymbol, m.price, v.quantity
                  FROM "quote"."matched" m
                  LEFT JOIN "quote"."total" v
                  ON m.tickersymbol = v.tickersymbol
                  and m.datetime =  v.datetime
                  where m.datetime between '2021-1-1' and '2021-12-31'
                  and m.tickersymbol LIKE 'VN30F21%'
                  AND v.quantity IS NOT NULL      
                  ORDER BY m.datetime ASC
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
                  where m.datetime between '2024-1-1' and '2024-12-31'
                  and m.tickersymbol LIKE 'VN30F24%'
                  AND v.quantity IS NOT NULL      
                  ORDER BY m.datetime ASC
            """)
            out_sample_data = cur.fetchall()
            print(f'Total number of tick: {len(out_sample_data)}')
            save_data(out_sample_data, 'database/2024.csv')
    

def save_data(data, file_path):
   df = pd.DataFrame(data, columns=['datetime', 'tickersymbol', 'price', 'quantity'])
   df['datetime'] = pd.to_datetime(df['datetime'])

   df.to_csv(file_path, index=False)
   print(f"Data saved to {file_path}")

def load_data(file_path):
   in_sample_data = pd.read_csv(file_path)
   df = pd.DataFrame(in_sample_data, columns=['datetime', 'tickersymbol', 'price', 'quantity'])
   df['datetime'] = pd.to_datetime(df['datetime'])
   # df['timestamp'] = pd.to_datetime(df['datetime']).dt.strftime('%H:%M:%S')
   unique_dates = df['datetime'].dt.strftime('%Y-%m-%d').unique().tolist()
   print(f"Unique dates: {len(unique_dates)}")

   df.set_index('datetime', inplace=True)
   # print(df.dtypes)

   df['price'] = pd.to_numeric(df['price'], errors='coerce')
   df['returns'] = df['price'].pct_change()
   df['volatility'] = df['returns'].rolling(window=5).std() * 100

   ohlc = df['price'].resample('D').ohlc()
   ohlc['volume'] = df['quantity'].resample('D').sum()
   ohlc['volatility'] = df['volatility'].resample('D').mean().round(2)
   ohlc = ohlc.dropna()
   # df.reset_index(inplace=True)
   # df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d')
   # df.set_index('datetime', inplace=True)


   return ohlc


# connect_db(True) # in-sample data
# connect_db(False) # out-sample data
