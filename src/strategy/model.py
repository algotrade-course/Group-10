import pandas as pd

class MovingAverageCrossoverStrategy:
    def compute_macd(self, data, short_ema=12, long_ema=26, signal_ema=9):
        data['MACD'] = data['close'].ewm(span=short_ema, adjust=False).mean() - data['close'].ewm(span=long_ema, adjust=False).mean()
        data['MACD_signal'] = data['MACD'].ewm(span=signal_ema, adjust=False).mean()
        data['Histogram'] = data['MACD'] - data['MACD_signal']
        return data

    def generate_signals(self, data, short_ema, long_ema, signal_ema, window):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        signals['sma_50'] = data['close'].rolling(window=window).mean()

        data = self.compute_macd(data, short_ema, long_ema, signal_ema)
        signals['MACD'] = data['MACD']

        # Buy and sell conditions using moving averages and MACD
        buy_condition = (data['MACD'] > data['MACD_signal']) & \
                        (data['MACD'] < 0) & (data['MACD_signal'] < 0) & \
                        (data['close'] > signals['sma_50'])
        # buy_condition = (data['MACD'] > data['MACD_signal']) & (data['close'] > signals['sma_50'])

        sell_condition = (data['MACD'] < data['MACD_signal']) & \
                         (data['MACD'] > 0) & (data['MACD_signal'] > 0) & \
                         (data['close'] < signals['sma_50'])
        # sell_condition = (data['MACD'] < data['MACD_signal']) & (data['close'] < signals['sma_50'])

        signals.loc[buy_condition, 'signal'] = 1.0
        signals.loc[sell_condition, 'signal'] = -1.0
        signals['positions'] = signals['signal'].diff()

        return signals, data