import streamlit as st
import pandas as pd
import plotly.express as px
from performance_analyzer import Portfolio, PerformanceAnalyzer


st.title("Portfolio Performance Analyzer")
st.caption(
    "Upload historical prices, define portfolio weights, "
    "and compare performance with a benchmark."
)

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type="csv"
)

if uploaded_file is not None:
    prices_preview = pd.read_csv(uploaded_file)
    if "date" not in prices_preview.columns:
        st.error("The CSV file must contain a 'date' column.")
        st.stop()
    available_columns = (
        prices_preview.columns
        .drop("date")
        .tolist()
    )
    
    if len(available_columns)<2:
        st.error(
            "The CSV file must contain at least one asset "
            "and one benchmark"
        )
        st.stop()
    with st.expander("Preview uploaded data"):
        st.dataframe(prices_preview)
    
    benchmark_column = st.selectbox(
        "Select the benchmark",
        available_columns
    )
    
    asset_columns = [
        column
        for column in available_columns
        if column != benchmark_column
    ]
    
    st.subheader("Portfolio weights")
    weights = {}
    default_weight = 1 / len(asset_columns)
    
    for asset in asset_columns:
        weights[asset] = st.number_input(
            f"{asset} weight",
            min_value=0.0,
            max_value=1.0,
            value=float(default_weight),
            step=0.01
        )
    
    total_weight = sum(weights.values())
    st.write(f"Total weight: {total_weight:.2%}")
    allocation_data = pd.DataFrame({
        "Asset": weights.keys(),
        "Weight": weights.values()
    })
    allocation_chart = px.pie(
        allocation_data,
        names="Asset",
        values="Weight",
        title="Portfolio allocation"
    )
    st.plotly_chart(
        allocation_chart,
        use_container_width=True
    )
    
    if st.button("Run analysis"):
        if abs(total_weight - 1.0) > 0.000001:
            st.error("Portfolio weights must sum to 100%.")
        else:
            try:
                uploaded_file.seek(0)
                portfolio = Portfolio(uploaded_file, weights, benchmark_column)
                analyzer = PerformanceAnalyzer(portfolio)
                st.subheader("Performance summary")
                st.dataframe(
                    analyzer.performance_summary(),
                    hide_index=True)
                chart_data = analyzer.comparison[
                    [
                        "portfolio_cumulative_return",
                        "benchmark_cumulative_return"
                    ]
                ]
                chart_data = chart_data * 100
                initial_date = portfolio.prices.index[0]
                chart_data.loc[initial_date] = [0.0, 0.0]
                chart_data = chart_data.sort_index()
                chart_data = chart_data.rename(columns={
                    "portfolio_cumulative_return": "Portfolio",
                    "benchmark_cumulative_return": "Benchmark"
                })
                
                st.subheader("Cumulative return (%)")
                st.line_chart(chart_data)
            except (ValueError, TypeError) as error:
                st.error(str(error))