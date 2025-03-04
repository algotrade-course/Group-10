from ..optimizer.position import *


def backtest(data, signals, loss_threshold, initial_asset=40000000):
    prev_date = None
    trading_data = data.copy()
    asset_value = initial_asset
    holdings = []
    count = 0
    trade: bool = False

    # Loop through data history
    for date in data.index:
        # Skip the first date
        if prev_date is None:
            prev_date = date
            continue
        cur_price = data['close'][date]
        histogram = data['Histogram'][date]

        # Close positions if conditions are met
        holdings, total_realized_pnl, total_unrealized_pnl, asset_value = close_positions(cur_price, asset_value, holdings, loss_threshold, date, histogram)

        # Update asset history
        if total_realized_pnl == 0:
            trading_data.loc[date, 'Asset'] = asset_value + total_unrealized_pnl
        else:
            trading_data.loc[date, 'Asset'] = asset_value

        # Ensure only one open contract at a time
        if holdings:
            prev_date = date
            continue

        # Buy if both ema lines are both below 0 line + macd line > signal line + sma uptrend.
        if (data['MACD'][date] > (data['MACD_signal'][date])) and \
           (data['close'][date] > signals['sma_50'][date]):
        #    (data['MACD'][date] < 0 and data['MACD_signal'][date] < 0) and \
            holdings, trade = open_position('long', cur_price, asset_value, holdings)
            # print("Buy at: ", date)

        # Sell if both ema lines are both above 0 + macd line < signal line + sma downtrend.
        elif (data['MACD'][date] < (data['MACD_signal'][date])) and \
             (data['close'][date] < signals['sma_50'][date]):
            #  (data['MACD'][date] > 0 and data['MACD_signal'][date] > 0) and \
            holdings, trade = open_position('short', cur_price, asset_value, holdings)
            # print("Sold at: ", date)

        if trade:
            count += 1

        prev_date = date  # Prepare for next iteration

    trading_data = trading_data.dropna()
    data = trading_data.copy()
    # print(trading_data['Asset'])
    print(f"\nTotal asset after 2 year: {asset_value:.2f}")
    print(f"Total transaction: {count}")
    return data