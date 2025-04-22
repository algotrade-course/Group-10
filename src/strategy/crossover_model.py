import numpy as np
from ..utils.visualize_data import plotChart
from ..utils.download_data import load_data

class MovingAverageCrossoverStrategy:
    def compute_macd(self, data, short_ema, long_ema, signal_ema, ema_window, plot=False):
        data['MACD'] = (data['close'].ewm(span=short_ema * 1, adjust=False).mean() - data['close'].ewm(span=long_ema * 1, adjust=False).mean()).fillna(0).round(2)
        data['MACD_signal'] = data['MACD'].ewm(span=signal_ema * 1, adjust=False).mean().fillna(0).round(2)
        data['Histogram'] = (data['MACD'] - data['MACD_signal']).fillna(0).round(2)
        data['EMA_50'] = data['close'].ewm(span=ema_window * 1, adjust=False).mean().fillna(0).round(2)
        if plot:
            plotChart(data)

        # data.reset_index(inplace=True)
        # data.to_csv('database/ohlc_2022.csv', index=False)
        # data.set_index('datetime', inplace=True)
        return data
