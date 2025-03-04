from typing import List


# Define the cut loss threshold and take profit threshold
CUT_LOSS_THRES = -8 
TAKE_PROFIT_THRES = 40 
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
    holdings: List[[str, float]]
):
    # YOUR CODE HERE
    deposit_required = calculate_margin(entry_point)
    if deposit_required > asset_value:
        print(f"Insufficient funds to open a {position_type} position at {entry_point} with current asset value: {asset_value:.2f}")
        return holdings, False
    else:
        holdings.append((position_type, entry_point))
        # asset_value -= deposit_required

    return holdings, True

def close_positions(
    cur_price: float,
    asset_value: float,
    holdings: List[[str, float]],
    loss_threshold: float,
    date: str,
    histogram: float
):

    total_realized_pnl = 0
    total_unrealized_pnl = 0
    updated_holdings = []
    if len(holdings) == 0:
        return holdings, total_realized_pnl, total_unrealized_pnl, asset_value

    for position_type, entry_point in holdings:
        # Calculate profit/loss for each position
        raw_pnl = (cur_price - entry_point) if position_type == 'long' else (entry_point - cur_price)
        pnl = raw_pnl - TRANSACTION_FEE
        
        # Check if the position should be closed based on the histogram or thresholds
        if (position_type == 'long' and histogram <= 0) or (position_type == 'short' and histogram >= 0) or \
           pnl <= loss_threshold:
            # Close position
            # print(f"Close at: {date} with profit: {pnl:.2f}")
            total_realized_pnl += (pnl * MULTIPLIER)
            # Update asset value when position is realized
            asset_value += total_realized_pnl
            
        else:
            # Keep position open
            total_unrealized_pnl += (raw_pnl * MULTIPLIER)
            updated_holdings.append((position_type, entry_point))

    return updated_holdings, total_realized_pnl, total_unrealized_pnl, asset_value