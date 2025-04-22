from typing import List


# Define the cut loss threshold and take profit threshold 
MULTIPLIER = 100000
TRANSACTION_FEE = 0.47
MARGIN_RATIO = 0.175
AR_TARGET = 0.8

def calculate_margin(price: float) -> float:
    margin_required = price * MARGIN_RATIO * MULTIPLIER
    deposit_required = margin_required / AR_TARGET
    return deposit_required

def open_position(
    position_type: str,
    entry_point: float,
    asset_value: float,
    date: str,
    holdings: List[[str, float]]
):
    # YOUR CODE HERE
    deposit_required = calculate_margin(entry_point)
    if deposit_required > asset_value:
        print(f"Insufficient funds to open a {position_type} position at {entry_point} with current asset value: {asset_value:.2f}")
        return holdings, False, True
    else:
        holdings.append((position_type, entry_point))
        # print(f"Open {position_type} position at {entry_point} at {date} with asset value: {asset_value:.2f}")
        # asset_value -= deposit_required

    return holdings, True, False

def close_positions(
    cur_price: float,
    asset_value: float,
    holdings: List[[str, float]],
    date: str,
    prev_date: str,
    close_price: float,
    histogram: float,
    take_profit: float,
    cut_loss: float
):

    total_realized_pnl = 0
    total_unrealized_pnl = 0
    updated_holdings = []
    pos_type = ""
    if len(holdings) == 0:
        return holdings, total_realized_pnl, total_unrealized_pnl, asset_value, pos_type
    
    # # Check if it's the end of the day
    # if date != prev_date:
    #     for position_type, entry_point in holdings:
    #         # Calculate profit/loss for each position
    #         raw_pnl = (close_price - entry_point) if position_type == 'long' else (entry_point - close_price)
    #         pnl = raw_pnl - TRANSACTION_FEE

    #         # Realize the profit/loss
    #         total_realized_pnl += (pnl * MULTIPLIER)
    #         asset_value += (pnl * MULTIPLIER)  # Update asset value
    #         print(f"Close at: {date} with profit: {pnl:.2f} at close price: {close_price:.2f}")

    #     # Clear all holdings
    #     holdings = []
    #     return holdings, total_realized_pnl, total_unrealized_pnl, asset_value
    

    for position_type, entry_point in holdings:
        # Calculate profit/loss for each position
        raw_pnl = (close_price - entry_point) if position_type == 'long' else (entry_point - close_price)
        pnl = raw_pnl - TRANSACTION_FEE
        
        # Check if the position should be closed based on the histogram or thresholds
        if (position_type == 'long' and histogram <= 0.5) or (position_type == 'short' and histogram >= -0.5) or \
           raw_pnl <= cut_loss or raw_pnl >= take_profit:
            # Close position
            total_realized_pnl += (pnl * MULTIPLIER)
            # Update asset value when position is realized
            asset_value += total_realized_pnl
            pos_type = position_type
            # print(f"Close at: {date} with profit: {pnl:.2f} at current price: {close_price:.2f} with histogram: {histogram:.2f}")
            
        else:
            # Keep position open
            total_unrealized_pnl += (raw_pnl * MULTIPLIER)
            updated_holdings.append((position_type, entry_point))

    return updated_holdings, total_realized_pnl, total_unrealized_pnl, asset_value, pos_type
