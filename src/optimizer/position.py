from typing import List


# Define the cut loss threshold and take profit threshold
CUT_LOSS_THRES = -8 
TAKE_PROFIT_THRES = 40 

def open_position(
    position_type: str,
    entry_point: float,
    holdings: List[[str, float]]
):
    # YOUR CODE HERE
    holdings.append((position_type, entry_point))

    return holdings

def close_positions(
    cur_price: float,
    holdings: List[[str, float]],
    loss_threshold: float,
    date: str,
    histogram: float
):
    total_realized_pnl = 0
    total_unrealized_pnl = 0
    updated_holdings = []

    for position_type, entry_point in holdings:
        # Calculate profit/loss for each position
        pnl = (cur_price - entry_point) if position_type == 'long' else (entry_point - cur_price)
        
        # Check if the position should be closed based on the histogram or thresholds
        if (position_type == 'long' and histogram <= 0) or (position_type == 'short' and histogram >= 0) or \
           pnl <= loss_threshold:
            # Close position
            # print(f"Close at: {date} with profit: {pnl:.2f}")
            total_realized_pnl += (pnl - 0.47)  # Subtracting the transaction cost
        else:
            # Keep position open
            if position_type == 'long':
                unrealized_pnl = cur_price - entry_point
            else:
                unrealized_pnl = entry_point - cur_price
            total_unrealized_pnl += unrealized_pnl
            updated_holdings.append((position_type, entry_point))

    return updated_holdings, total_realized_pnl, total_unrealized_pnl