import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Function to calculate weights based on the selected strategy
def calculate_weights(returns, strategy):
    if strategy == "Equal Weight":
        return np.ones(len(returns.columns)) / len(returns.columns)  # Equal weight for all stocks

    elif strategy == "Risk Parity":
        # Simple risk parity: inversely proportional to volatility
        weights = 1 / returns.std(axis=0)
        return weights / weights.sum()  # Normalize to sum to 1

    elif strategy == "Risk Allocation":
        # Risk allocation: weights proportional to volatility
        weights = returns.std(axis=0)
        return weights / weights.sum()  # Normalize to sum to 1

    elif strategy == "Momentum":
        # Momentum: based on last period's returns
        weights = returns.iloc[-1]
        return weights / weights.sum()  # Normalize to sum to 1

    return np.ones(len(returns.columns)) / len(returns.columns)  # Default to equal weight if method not recognized

# Portfolio Performance Calculation Function
def calculate_portfolio_performance(stocks, start_date, end_date, lookup_period, initial_cash, strategy):
    # Download stock price data
    data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']

    # Check if data is empty
    if data.empty:
        st.warning("No data was retrieved for the selected date range and stocks.")
        return None, None, None, None

    # Normalize the data
    normalized_data = data / data.iloc[0]

    # Create lists to store portfolio values and weights
    portfolio_values = []
    weights_history = []

    # Frequency mapping to resample data
    frequency_mapping = {
        'Weekly': 'W',
        'Monthly': 'M',
        'Quarterly': 'Q'
    }

    # Set resampling frequency
    freq = frequency_mapping[lookup_period]

    # Initialize weights as equal for the first calculation
    weights = calculate_weights(normalized_data.pct_change().dropna(), strategy)

    # Loop through the date range, resampling at the specified frequency
    for date in normalized_data.resample(freq).mean().index:
        # Calculate portfolio value at this point
        portfolio_value = (normalized_data.loc[:date] * weights).sum(axis=1).iloc[-1]
        portfolio_values.append(portfolio_value)

        # Calculate returns for each stock over the period
        returns = normalized_data.loc[:date].pct_change().dropna()

        # Update weights based on the selected strategy
        weights = calculate_weights(returns, strategy)

        # Set any negative weights to zero
        weights[weights < 0] = 0

        # Normalize the weights to sum to 1
        weights /= weights.sum() if weights.sum() > 0 else 1  # Prevent division by zero

        weights_history.append(weights)

    # Create a portfolio value series
    portfolio_value_series = pd.Series(portfolio_values, index=normalized_data.resample(freq).mean().index)

    # Create a DataFrame for weights
    weights_df = pd.DataFrame(weights_history, columns=stocks, index=normalized_data.resample(freq).mean().index)

    # Calculate returns for the same frequency
    portfolio_returns = portfolio_value_series.pct_change() * 100

    return portfolio_value_series, data, portfolio_returns, weights_df

# Main Streamlit Interface
st.title('Investment Portfolio Creator')

# User input: Select stocks
available_stocks = ['AAPL', 'ADBE', 'AEYE', 'AMD', 'AMZN', 'ANET', 'ARKG', 'ARKK', 'ASML', 'AVGO', 
                    'CELH', 'CMG', 'COST', 'CRM', 'CYBR', 'FTI', 'FTNT', 'GOOGL', 'HUBS', 'INTC', 
                    'KLAC', 'LLY', 'LPLA', 'LRCX', 'MA', 'MARA', 'MELI', 'META', 'MRVL', 'MSFT', 
                    'MSI', 'MSTR', 'MU', 'NFLX', 'NOW', 'NVDA', 'ORCL', 'OXY', 'PANW', 'QCOM', 
                    'SMCI', 'SMH', 'TSLA', 'TSM', 'V', 'WDAY', 'XLE', 'XLF']
selected_stocks = st.multiselect('Select stocks for your portfolio', available_stocks)

# User input: Select date range
start_date = st.date_input('Start date')
end_date = st.date_input('End date')

# Validate date input
if start_date >= end_date:
    st.warning('The start date must be earlier than the end date.')

# User input: Select lookup period
lookup_options = ['Weekly', 'Monthly', 'Quarterly']
lookup_period = st.selectbox('Select lookup period', lookup_options)

# User input: Initial cash
initial_cash = st.number_input('Initial Cash Amount', min_value=1000.0, value=100000.0)

# User input: Select weight calculation strategy
strategies = ['Equal Weight', 'Risk Parity', 'Risk Allocation', 'Momentum']
selected_strategies = st.multiselect('Select weight calculation strategies', strategies)

# Display button to start the simulation
if st.button('Simulate Portfolio'):
    if len(selected_stocks) > 0 and len(selected_strategies) > 0:
        portfolio_results = {}

        for strategy in selected_strategies:
            # Call portfolio performance function for each strategy
            portfolio_value, stock_data, portfolio_returns, weights_df = calculate_portfolio_performance(
                selected_stocks, start_date, end_date, lookup_period, initial_cash, strategy
            )

            if portfolio_value is not None:
                portfolio_results[strategy] = (portfolio_value, portfolio_returns, weights_df)

        # Plot portfolio values for each strategy
        st.subheader('Portfolio Value Over Time by Strategy')
        fig = go.Figure()

        for strategy, (portfolio_value, _, _) in portfolio_results.items():
            fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value.values, mode='lines', name=strategy))

        fig.update_layout(title='Portfolio Value Over Time by Strategy',
                            xaxis_title='Date',
                            yaxis_title='Portfolio Value')
        st.plotly_chart(fig)

        # Display stock data as a table
        st.subheader('Stock Prices')
        st.dataframe(stock_data)

        # Show summary metrics for each strategy
        for strategy, (portfolio_value, portfolio_returns, weights_df) in portfolio_results.items():
            st.write(f'**Strategy: {strategy}**')
            st.write(f'Total Return: {((portfolio_value[-1] / portfolio_value[0]) - 1) * 100:.2f}%')

            # Calculate and display Sharpe Ratio
            risk_free_rate = 0.01  # Example risk-free rate
            sharpe_ratio = (portfolio_returns.mean() - risk_free_rate) / portfolio_returns.std()
            st.write(f'Sharpe Ratio: {sharpe_ratio:.2f}')

            # Plot weights as a bar chart for each strategy
            st.subheader(f'Weights Over Time for {strategy}')
            fig3 = go.Figure()

            # Create bar charts for weights of each stock
            for stock in selected_stocks:
                fig3.add_trace(go.Bar(x=weights_df.index, y=weights_df[stock], name=stock))

            # Update layout for the bar chart
            fig3.update_layout(title=f'Weights of Each Stock Over Time for {strategy}',
                                xaxis_title='Date',
                                yaxis_title='Weights',
                                barmode='stack')  # Change to 'group' if you want side-by-side bars

            st.plotly_chart(fig3)

    else:
        st.warning('Please select stocks and at least one strategy for comparison.')
