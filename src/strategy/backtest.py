from .position import open_position, close_positions
from tqdm import tqdm
from collections import deque


def backtest(ohlc, take_profit, cut_loss, initial_asset):
    prev_date = None
    trading_data = ohlc.copy()
    asset_value = initial_asset
    holdings = []
    count = 0
    trade: bool = False
    escape: bool = False
    not_buy: bool = False
    not_sell: bool = False

    macd_history = deque(maxlen=3)


    for index, row in tqdm(ohlc.iterrows(), total=len(ohlc)):
        # Skip the first date
        if prev_date is None:
            prev_date = index
            continue
        date = index
        curr_price = close_price = ohlc['close'][date]
        histogram = ohlc['Histogram'][date]
        prev_histogram = ohlc['Histogram'][prev_date]
        macd = ohlc['MACD'][date]
        macd_signal = ohlc['MACD_signal'][date]
        ema_50 = ohlc['EMA_50'][date]
        prev_price = ohlc['close'][prev_date]
        macd_history.append(macd)

        holdings, total_realized_pnl, total_unrealized_pnl, asset_value, pos_type = close_positions(curr_price, asset_value, holdings, date, prev_date, close_price, histogram, take_profit, cut_loss)
        # if total_realized_pnl > 35:
        #     if pos_type == 'long':
        #         not_buy = True
        #     elif pos_type == 'short':
        #         not_sell = True

         # Update asset history
        if total_realized_pnl == 0:
            trading_data.loc[date, 'Asset'] = asset_value + total_unrealized_pnl
        else:
            trading_data.loc[date, 'Asset'] = asset_value

        # Ensure only one open contract at a time
        if holdings:
            prev_date = date
            continue
        macd_derivative = (macd_history[-1] - macd_history[0]) / len(macd_history)  # Calculate the derivative of MACD
        
        buy_signal = (macd > macd_signal) and (curr_price >= ema_50) and (histogram <= 3) and (macd_derivative > 0)
        sell_signal = (macd < macd_signal) and (curr_price <= ema_50) and (histogram >= -3) and (macd_derivative < 0)

        if buy_signal:
            # if not_buy == False:
            # Buy condition
            # print(f"Open long position at {date} with macd {macd:.2f}, macd_signal {macd_signal:.2f}, histogram {histogram:.2f} and price {curr_price:.2f}")
            holdings, trade, escape = open_position('long', curr_price, asset_value, date, holdings)
            # elif not_buy == True:
            #     not_buy = False
        elif sell_signal:
        # Sell condition
            # if not_sell == False:
            # print(f"Open short position at {date} with macd {macd:.2f}, macd_signal {macd_signal:.2f}, histogram {histogram:.2f} and price {curr_price:.2f}")
            holdings, trade, escape = open_position('short', curr_price, asset_value, date, holdings)
            # elif not_sell == True:
            #     not_sell = False
        if trade:
            count += 1
            trade = False
        if escape:
            print(f"Escape at: {date} with asset value: {asset_value:.2f}")
            print(f"MACD: {macd:.2f}, MACD_signal: {macd_signal:.2f}, Histogram: {histogram:.2f}")
            print(f"Current price: {curr_price:.2f}, EMA_50: {ema_50:.2f}")
            break

        prev_date = date  # Prepare for next iteration

    trading_data = trading_data.dropna()
    data = trading_data.copy()
    trading_data['Asset'] = trading_data['Asset'].round(0).astype(int)
    trading_data['Asset'].to_csv('database/asset.csv', index=True)
    print(f"\nTotal asset after a year: {asset_value:.2f}")
    print(f"Total transaction: {count}")
    return data, count