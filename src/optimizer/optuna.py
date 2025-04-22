from ..metrics.evaluation import sharpeRatio
from ..strategy.backtest import backtest
from ..strategy.crossover_model import MovingAverageCrossoverStrategy



def objective(trial, ohlc):
    short_ema = trial.suggest_int('short_ema', 7, 14)
    long_ema = trial.suggest_int('long_ema', 14, 28)
    signal_ema = trial.suggest_int('signal_ema', 7, 14)
    window = trial.suggest_int('window', 40, 60)

    CUT_LOSS_THRES = trial.suggest_int('CUT_LOSS_THRES', -20, -10)
    TAKE_PROFIT_THRES = trial.suggest_int('TAKE_PROFIT_THRES', 15, 30)
    INITIAL_ASSET = 50000000

    strategy = MovingAverageCrossoverStrategy()
    data = strategy.compute_macd(ohlc, short_ema, long_ema, signal_ema, window)
    data, _ = backtest(data, TAKE_PROFIT_THRES, CUT_LOSS_THRES, INITIAL_ASSET)

   #  data['daily_return'] = data['Asset'].pct_change()
    data = data.dropna()
    sharpe_ratio = sharpeRatio(data)
    return sharpe_ratio
