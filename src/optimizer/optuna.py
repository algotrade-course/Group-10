from ..metrics.evaluation import sharpeRatio
from ..strategy.backtest import backtest
from ..strategy.model import MovingAverageCrossoverStrategy

def objective(trial, ohlc):
    short_ema = trial.suggest_int('short_ema', 7, 20)
    long_ema = trial.suggest_int('long_ema', 21, 40)
    signal_ema = trial.suggest_int('signal_ema', 7, 21)
    window = trial.suggest_int('window', 40, 80)
    CUT_LOSS_THRES = trial.suggest_int('CUT_LOSS_THRES', -15, -5)

    strategy = MovingAverageCrossoverStrategy()
    signals, data = strategy.generate_signals(ohlc, short_ema, long_ema, signal_ema, window)
    data = backtest(data, signals, CUT_LOSS_THRES)

   #  data['daily_return'] = data['Asset'].pct_change()
    data = data.dropna()
    sharpe_ratio = sharpeRatio(data)
    return sharpe_ratio
