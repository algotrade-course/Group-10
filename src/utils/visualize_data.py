import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np

def plot(data, signals):
  fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

  # --- Price Chart with Moving Averages ---
  ax1.plot(data['close'], label='VN Future Closing Price', alpha=0.5)
  ax1.plot(signals['sma_50'], label='50-Day SMA', alpha=0.8, color="purple")

  ax1.scatter(signals.loc[signals.positions == 1.0].index,
              signals.sma_50[signals.positions == 1.0],
              label='Buy Signal', marker='^', color='g', s=100)
  ax1.scatter(signals.loc[signals.positions == -1.0].index,
              signals.sma_50[signals.positions == -1.0],
              label='Sell Signal', marker='v', color='r', s=100)

  ax1.set_title('VNF Moving Average Crossover & 50-Day SMA')
  ax1.set_ylabel('Price (USD)')
  ax1.legend()
  ax1.grid(True)

  # --- MACD Indicator ---
  ax2.plot(data['MACD'], label="MACD Line", color='blue', alpha=0.8)
  ax2.plot(data['MACD_signal'], label="Signal Line", color='red', alpha=0.8)
  ax2.bar(data.index, data['Histogram'], label="Histogram", color=np.where(data['Histogram'] >= 0, 'green', 'brown'))

  ax2.set_title('MACD Indicator')
  ax2.set_xlabel('Date')
  ax2.legend()
  ax2.grid(True)

  plt.show()

# ohlc = load_data('database/indata.csv')
# strategy = MovingAverageCrossoverStrategy()
# signals, data = strategy.generate_signals(ohlc, 12, 25, 17, 49)
# plot(data, signals)

# Draw the Candlestick chart
# mpf.plot(ohlc, type='candle', volume=True, title='VN30F1M Candlestick Chart (2023-2024)', style='charles')


