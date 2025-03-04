from src.utils.download_data import load_data
from src.utils.visualize_data import plot
from src.strategy.model import MovingAverageCrossoverStrategy
from src.strategy.backtest import backtest
from src.metrics.evaluation import evaluation
from src.optimizer.optuna import objective
import optuna
import json


def main(in_sample=True):
   INITIAL_ASSET = 60000000
   if in_sample:
      # load in-sample data and apply the strategy
      ohlc = load_data('database/indata.csv')
      strategy = MovingAverageCrossoverStrategy()
      signals, data = strategy.generate_signals(ohlc, 12, 26, 9, 50) # default parameters for MACD
      # plot(data, signals)

      # backtest the strategy and evaluate the performance
      data = backtest(data, signals, -8, INITIAL_ASSET)
      evaluation(data)

      # optimize the strategy
      seed_value = 0
      sampler = optuna.samplers.TPESampler(seed=seed_value)
      study = optuna.create_study(sampler=sampler, direction='maximize')
      study.optimize(lambda trial: objective(trial, ohlc), n_trials=150, show_progress_bar=True)

      print("Best parameters: ", study.best_params)
      print("Best Sharpe ratio: ", study.best_value)

      # extract the best parameters and re-backtest the strategy
      with open('config/best_params.json', 'w') as f:
         json.dump(study.best_params, f)
         print("Best parameters saved")
      short_ema = study.best_params['short_ema']
      long_ema = study.best_params['long_ema']
      signal_ema = study.best_params['signal_ema']
      window = study.best_params['window']
      CUT_LOSS_THRES = study.best_params['CUT_LOSS_THRES']
      signals, data = strategy.generate_signals(ohlc, short_ema, long_ema, signal_ema, window)
      data = backtest(data, signals, CUT_LOSS_THRES, INITIAL_ASSET)
      evaluation(data)
   else:
      with open('config/best_params.json', 'r') as f:
         best_params = json.load(f)
      # load out-sample data and apply the strategy
      ohlc = load_data('database/outdata.csv')
      strategy = MovingAverageCrossoverStrategy()
      signals, data = strategy.generate_signals(ohlc, best_params['short_ema'], best_params['long_ema'], best_params['signal_ema'], best_params['window'])
      data = backtest(data, signals, best_params['CUT_LOSS_THRES'], INITIAL_ASSET)
      # signals, data = strategy.generate_signals(ohlc, 12, 25, 17, 49)
      # data = backtest(data, signals, -8, 40000000)
      evaluation(data)

if __name__ == "__main__":
   # main(True)
   main(False)