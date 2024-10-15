# Investment Portfolio Creator

This application allows users to create and simulate an investment portfolio using various stocks and weight calculation strategies. It uses historical stock price data to evaluate portfolio performance over a specified period.

## Features

- Select stocks from a predefined list (Apple, Google, Amazon, Microsoft, Tesla).
- Choose a date range for the simulation.
- Set an initial cash amount for the portfolio.
- Select a lookup period for resampling (weekly, monthly, quarterly).
- Choose from different weight calculation strategies:
  - Equal Weight
  - Risk Parity
  - Risk Allocation
  - Market Neutral
  - Momentum
- Visualize portfolio value over time for each strategy.
- Display stock price data in a table.
- Calculate and show summary metrics including total return and Sharpe Ratio.

## Technologies Used

- **Python**: Main programming language.
- **Streamlit**: Web application framework.
- **yfinance**: Library for fetching financial data.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical operations.
- **Plotly**: Interactive plotting library for visualizations.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run portfolio_app.py  # Replace `app.py` with your actual script name
   ```

## Usage

1. Open the application in your web browser (the terminal will show the URL).
2. Select stocks, date range, lookup period, initial cash amount, and weight calculation strategies.
3. Click the "Simulate Portfolio" button to generate the portfolio performance results and visualizations.

## License

This project is licensed under the MIT License.
