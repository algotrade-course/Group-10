import numpy as np
import matplotlib.pyplot as plt

def maximumDrawdown(data):
   # For each day, calculate the peak of asset value since inception
   data['peak'] = data.apply(lambda row: data.loc[:row.name, 'Asset'].max(), axis=1)

   # For each day, calculate asset drawdown
   data['drawdown'] = data['Asset']/data['peak'] - 1

   # max drawdown is the most negative value
   mdd = data['drawdown'].min() * 100
   print(f"Max Drawdown: {mdd:.2f}%")
   return mdd

def sharpeRatio(data):
  daily_return = data['Asset'][1:].to_numpy() / data['Asset'][:-1].to_numpy() - 1
  # Calculate the Sharpe Ratio by daily return with annualization
  trading_days_per_year = 252
  risk_free_rate = 0.03 # e.g. government bonds interest is 3% per year

  # annual standard deviation
  annual_std = np.sqrt(trading_days_per_year) * np.std(daily_return)

  # annual return
  annual_return = trading_days_per_year * np.mean(daily_return) - risk_free_rate

  # annualized Sharpe ratio
  sharpe = annual_return / annual_std
  print(f"Sharpe ratio: {sharpe:.2f}")
  return sharpe

def returnRate(data):
   # Plot asset value over time
  data['Asset'].plot(kind='line', figsize=(8, 4), title='Asset Over Time')
  plt.gca().spines[['top', 'right']].set_visible(False)
  plt.show()

  cur_asset_value = data['Asset'].iloc[-1]
  init_asset_value = data['Asset'].iloc[0]
  # Percentage of return
  accum_return_rate = (cur_asset_value / init_asset_value - 1) * 100
  print(f"Return rate: {accum_return_rate:.2f}")
  return accum_return_rate

def evaluation(data):
  accum_return_rate = returnRate(data)
  sharpe = sharpeRatio(data)
  mdd = maximumDrawdown(data)