import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, file_path, weights, benchmark_column):
        self.file_path = file_path
        self.prices = self.load_prices()
        self.benchmark_column = benchmark_column
        self.weights = weights
        self.validate_weights()
        self.asset_returns = self.calculate_asset_returns()
        self.portfolio_returns = self.calculate_portfolio_returns()
        self.benchmark_returns = self.calculate_benchmark_returns()
        
    def load_prices(self):
        prices = pd.read_csv(
            self.file_path,
            parse_dates=["date"],
            index_col="date"
        )
        prices = prices.sort_index()
        
        if prices.index.duplicated().any():
            raise ValueError("Duplicate dates found.")

        if prices.isna().any().any():
            raise ValueError("Missing values found.")
        
        if (prices<=0).any().any():
            raise ValueError("Prices must be positive.")
        
        return prices
    
    def validate_weights(self):
        asset_columns = self.prices.columns.drop(self.benchmark_column)
        
        if set(asset_columns) != set(self.weights.keys()):
            raise ValueError("Weights must match portfolio assets.")
        
        total_weight = sum(self.weights.values())
        if not np.isclose(total_weight, 1.0):
            raise ValueError("Weights must sum to 1.")
    
    def calculate_asset_returns(self):
        asset_prices = self.prices.drop(columns=self.benchmark_column)
        asset_returns = asset_prices.pct_change().dropna()
        return asset_returns
    
    def calculate_portfolio_returns(self):
        weights_series = pd.Series(self.weights)
        weighted_returns = self.asset_returns.mul(weights_series)
        portfolio_returns = weighted_returns.sum(axis=1)
        return portfolio_returns
    
    def calculate_benchmark_returns(self):
        benchmark_returns = self.prices[self.benchmark_column].pct_change().dropna()
        return benchmark_returns
    
class PerformanceAnalyzer:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.comparison = self.compare_performance()
        self.outperformance_ratio = self.calculate_outperformance_ratio()
    
    def compare_performance(self):
        comparison = pd.DataFrame({
            "portfolio_return": self.portfolio.portfolio_returns,
            "benchmark_return": self.portfolio.benchmark_returns
        })

        comparison["excess_return"] = (
            comparison["portfolio_return"]
            - comparison["benchmark_return"]
        )
        portfolio_growth_factor = (1 + comparison["portfolio_return"])
        portfolio_cumulative_factor = portfolio_growth_factor.cumprod()
        comparison["portfolio_cumulative_return"] = portfolio_cumulative_factor - 1
        
        benchmark_growth_factor = (1 + comparison["benchmark_return"])
        benchmark_cumulative_factor = benchmark_growth_factor.cumprod()
        comparison["benchmark_cumulative_return"] = benchmark_cumulative_factor - 1
        
        comparison["cumulative_excess_return"] = (
            comparison["portfolio_cumulative_return"] 
            - comparison["benchmark_cumulative_return"]
        )
        
        return comparison
    
    def calculate_outperformance_ratio(self):
        
        outperforming_days = (
            self.comparison["excess_return"] > 0
        ).sum()
        
        outperformance_ratio = (
            outperforming_days / len(self.comparison)
        )
        
        return outperformance_ratio
    
    def calculate_annualized_volatility(self):
        portfolio_daily_volatility = (
            self.comparison["portfolio_return"].std()
        )
        benchmark_daily_volatility = (
            self.comparison["benchmark_return"].std()
        )
        portfolio_annualized_volatility = (
            portfolio_daily_volatility*np.sqrt(252)
        )
        benchmark_annualized_volatility = (
            benchmark_daily_volatility*np.sqrt(252)
        )
        return portfolio_annualized_volatility, benchmark_annualized_volatility
    
    def performance_summary(self):
        last_row = self.comparison.iloc[-1]
        
        portfolio_volatility, benchmark_volatility = (
            self.calculate_annualized_volatility()
        )
        
        summary = pd.DataFrame({
            "Metric": [
                "Portfolio cumulative return",
                "Benchmark cumulative return",
                "Cumulative outperformance",
                "Outperforming days",
                "Portfolio annualized volatility",
                "Benchmark annualized volatility"
            ],
            "Value (%)": [
                last_row["portfolio_cumulative_return"] * 100,
                last_row["benchmark_cumulative_return"] * 100,
                last_row["cumulative_excess_return"] * 100,
                self.outperformance_ratio * 100,
                portfolio_volatility * 100,
                benchmark_volatility * 100
            ]
        })

        summary["Value (%)"] = summary["Value (%)"].round(2)
        
        return summary
        
def main():

    file_path = "prices.csv"
    benchmark_column = "Benchmark"
    
    weights = {
        "Microsoft": 0.40,
        "LVMH": 0.35,
        "Euro_Gov_Bond": 0.25
    }

    portfolio = Portfolio(file_path, weights, benchmark_column)
    analyzer = PerformanceAnalyzer(portfolio)
    summary = analyzer.performance_summary()
    print(summary)

if __name__ == "__main__":
    main()