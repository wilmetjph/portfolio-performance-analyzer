# Portfolio Performance Analyzer

A Python and Streamlit application for analyzing a portfolio's historical performance against a selected benchmark.

[Open the Portfolio Performance Analyzer](https://wilmet-portfolio-analyzer.streamlit.app)

## Features

- Upload historical asset prices from a CSV file
- Select a benchmark dynamically
- Define portfolio weights through an interactive interface
- Validate portfolio weights and input data
- Calculate daily and cumulative returns
- Compare portfolio and benchmark performance
- Measure cumulative outperformance and annualized volatility
- Display a performance summary, allocation chart and cumulative return chart

## CSV format

- a column named `date`
- at least one portfolio asset
- one column that can be selected as the benchmark
- positive historical prices without missing values

## Installation and usage

1. Install the required libraries:

```bash
pip install -r requirements.txt
````

2. Start the Streamlit application:

```
streamlit run app.py
```

3. Upload a compatible CSV file, select the benchmark and define the portfolio weights

4. Ensure that the weights total 100%, then click Run Analysis.

## Project structure

```text
portfolio-performance-analyzer/
├── app.py                    # Streamlit interface
├── performance_analyzer.py   # Portfolio and performance calculations
├── prices.csv                # Example dataset
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Future improvements

- Sharpe and Sortino ratios
- Maximum drawdown
- Tracking error and information ratio
- Additional charts and reporting options
- More flexible date-column selection
