import argparse
from src.utils.download_data import load_data
from src.strategy.crossover_model import MovingAverageCrossoverStrategy
from src.strategy.backtest import backtest
from src.metrics.evaluation import evaluation
from src.optimizer.optuna import objective
import optuna
from optuna.visualization import plot_optimization_history
import json

def main(initial_asset, cut_loss, take_profit, in_sample, optimize, plot, data_file, optimize_file):
    if in_sample:
        ohlc = load_data(data_file)
        strategy = MovingAverageCrossoverStrategy()
        ohlc = strategy.compute_macd(ohlc, 12, 26, 9, 50, plot)  # default parameters for MACD

        # Backtest the strategy and evaluate the performance
        data, count = backtest(ohlc, take_profit, cut_loss, initial_asset)
        evaluation(data, count)

        if optimize:
            seed_value = 42
            sampler = optuna.samplers.TPESampler(seed=seed_value)
            study = optuna.create_study(sampler=sampler, direction='maximize')
            study.optimize(lambda trial: objective(trial, ohlc), n_trials=100, show_progress_bar=True)
            
            plot_optimization_history(study).show()
            print("Best parameters: ", study.best_params)
            print("Best Sharpe ratio: ", study.best_value)

            # Extract the best parameters and re-backtest the strategy
            with open(optimize_file, 'w') as f:
                json.dump(study.best_params, f)
                print("Best parameters saved")
            short_ema = study.best_params['short_ema']
            long_ema = study.best_params['long_ema']
            signal_ema = study.best_params['signal_ema']
            window = study.best_params['window']
            take_profit = study.best_params['TAKE_PROFIT_THRES']
            cut_loss = study.best_params['CUT_LOSS_THRES']
            ohlc = strategy.compute_macd(ohlc, short_ema, long_ema, signal_ema, window, plot)
            data, count = backtest(ohlc, take_profit, cut_loss, initial_asset)
            evaluation(data, count)
    else:
        with open(optimize_file, 'r') as f:
            best_params = json.load(f)
        # Load out-sample data and apply the strategy
        ohlc = load_data(data_file)
        strategy = MovingAverageCrossoverStrategy()
        ohlc = strategy.compute_macd(ohlc, best_params['short_ema'], best_params['long_ema'], best_params['signal_ema'], best_params['window'], plot)
        data, count = backtest(ohlc, best_params['TAKE_PROFIT_THRES'], best_params['CUT_LOSS_THRES'], initial_asset)
        evaluation(data, count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trading Strategy Backtesting and Optimization")
    parser.add_argument("--initial_asset", type=int, default=50000000, help="Initial asset value (default: 50000000)")
    parser.add_argument("--cut_loss", type=int, default=-12, help="Cut loss threshold (default: -15)")
    parser.add_argument("--take_profit", type=int, default=24, help="Take profit threshold (default: 25)")
    parser.add_argument("--in_sample", type=str, default="True", help="In-sample backtesting (default: True, accepts 'True' or 'False')")
    parser.add_argument("--optimize", type=str, default="False", help="Optimize hyperparameters (default: False, accepts 'True' or 'False')")
    parser.add_argument("--plot", type=str, default="False", help="Plot input data (default: False, accepts 'True' or 'False')")
    parser.add_argument("--data_file", type=str, default="database/2024.csv", help="Path to the data file (default: database/2021.csv)")
    parser.add_argument("--optimize_file", type=str, default="config/best_params.json", help="Path to the optimization file (default: config/best_params.json)")

    args = parser.parse_args()

    # Convert string inputs for boolean arguments to actual booleans
    in_sample = args.in_sample.lower() == "true"
    optimize = args.optimize.lower() == "true"
    plot = args.plot.lower() == "true"

    main(
        initial_asset=args.initial_asset,
        cut_loss=args.cut_loss,
        take_profit=args.take_profit,
        in_sample=in_sample,
        optimize=optimize,
        plot=plot,
        data_file=args.data_file,
        optimize_file=args.optimize_file
    )