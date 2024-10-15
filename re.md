# Investment Portfolio Creator

This project is a Streamlit-based web application for creating and simulating investment portfolios using different strategies. It allows users to select stocks, choose a date range, apply various portfolio weighting strategies, and visualize the portfolio performance over time.

## Features

- Stock selection from a predefined list of available stocks.
- Portfolio value calculation and simulation based on the following strategies:
  - **Equal Weight**: Assigns equal weight to all selected stocks.
  - **Risk Parity**: Weights are inversely proportional to the volatility of each stock.
  - **Risk Allocation**: Weights are proportional to the volatility of each stock.
  - **Momentum**: Weights are based on the performance of the stocks in the previous period.
- Visualization of portfolio value and stock weights over time.
- Calculation of Sharpe Ratio for each strategy.
- Flexible frequency resampling for portfolio updates (Weekly, Monthly, Quarterly).

## How to Run the Application

1. Clone the repository:

    ```
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```
    cd portfolio-creator
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:

    ```
    streamlit run app.py
    ```

## Requirements

- Python 3.8 or higher
- Required libraries (see `requirements.txt`)

## Example Workflow

1. Select one or more stocks from the list (e.g., AAPL, AMZN, MSFT).
2. Choose a date range for your portfolio simulation.
3. Choose a lookup period (Weekly, Monthly, or Quarterly).
4. Enter an initial cash amount for the portfolio.
5. Select one or more weight calculation strategies (Equal Weight, Risk Parity, etc.).
6. Click "Simulate Portfolio" to visualize the portfolio value over time for each selected strategy.

## License

This project is licensed under the MIT License.
