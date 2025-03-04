## 1. Trading Hypothesis
A crossover between short-term and long-term momentum signals can indicate potential trading opportunities. This strategy is more effective in trending markets and on higher timeframes, where price movements follow a clearer direction. However, in ranging markets or on lower timeframes, it often generates false signals due to market noise and frequent reversals. To improve accuracy and filter out weak signals, an additional trend confirmation indicator is used to ensure trades align with the overall market direction.

## 2. Data
- **Target Market**: VN30 Index Future Contract – VN30F1
- **Data Source**: API from AlgoTrade Database
- **Data Period**: Divided into two types:
  - In-sample data: from 01-01-2023 to 31-12-2024
  - Out-sample data: from 01-01-2021 to 31-12-2022
- **How to Get the Input Data?**
  - Fetching by using SQL command from API AlgoTrade

## 3. Data Processing
- After fetching the data into a list, it is converted into a Pandas DataFrame.
- The dataset is then saved as a CSV file for future use.
- The datetime column is set as the index, and the price column is converted to a numeric format. The data is resampled to a daily frequency, computing Open, High, Low, and Close (OHLC) values for each day. Any days without trading activity are removed by dropping rows containing NaN values.
- Finally, the processed OHLC dataset is visualized using a candlestick chart, providing a clear graphical representation of price trends and trading volumes over time.

## 4. Implementation
- Download libraries from `requirements.txt`.
- Toggle the parameter of the `connect_db` function in `utils/download_data.py` to download both in-sample and out-sample datasets. I already save both the datasets into csv files for later usage.
- Run the `main` function to see the result of the strategy on out-sample data. If you want to test the in-sample data, just modify `main(True)`.

## 5. In-sample Backtesting
- **Data**: Backtest on data of 2 years from 2023 to 2024
- **Initial Parameters** (default parameters of MACD indicator):
  - `short_ema = 12`
  - `long_ema = 26`
  - `signal_ema = 9`
  - `window_sma = 50`
  - `CUT_LOSS_THRES = -8`
  - `INITIAL_ASSET = 60000000 (60 million)`
- **Result**:
  - With initial parameters:
    - Total asset after 2 years: 69404000.00
    - Total transactions: 172
    - Return rate: 15.67%
    - Sharpe ratio: 0.32
    - Max Drawdown: -16.84%
  - ![Initial Parameters Result](image/initial.png)

## 6. Optimization
- Using the Optuna library to update the hyper-parameters:
  ```python
  short_ema = trial.suggest_int('short_ema', 7, 20)
  long_ema = trial.suggest_int('long_ema', 21, 40)
  signal_ema = trial.suggest_int('signal_ema', 7, 21)
  window = trial.suggest_int('window', 40, 80)
  CUT_LOSS_THRES = trial.suggest_int('CUT_LOSS_THRES', -15, -5)
  seed_value = 0

- **After Optimization parameters**:
  - `short_ema = 12`
  - `long_ema = 32`
  - `signal_ema = 14`
  - `window_sma = 48`
  - `CUT_LOSS_THRES = -9`
- **Result**:
  - With optimized parameters:
   - Total asset after 2 year: 61050000.00
   - Total transaction: 143
   - Return rate: 52.62%
   - Sharpe ratio: 0.83
   - Max Drawdown: -20.06%
![alt text](image/optimized.png)

## 7. Out-sample Backtesting
- **Data**: Backtest on data of 2 years from 2021 to 2022
- **Parameters**: Take from the most optimized parameters of in-sample data
  - `short_ema = 12`
  - `long_ema = 32`
  - `signal_ema = 14`
  - `window_sma = 48`
  - `CUT_LOSS_THRES = -9`
- **Result**:
   - Total asset after 2 year: 69330000.00
   - Total transaction: 173
   - Return rate: 21.75%
   - Sharpe ratio: 0.39
   - Max Drawdown: -55.48%
![alt text](image/outtesting.png)

