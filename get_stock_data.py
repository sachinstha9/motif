import datetime
import pandas as pd
import yfinance as yf

def get_combined_tech_stocks(tickers):
    # Calculate the date range for the last 15 years
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=15 * 365)

    all_data = {}

    print(
        f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}..."
    )

    for ticker in tickers:
        print(f"Downloading data for {ticker}...")

        # Fetch historical data
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            print(f"Warning: No data found for {ticker}")
            continue

        # Flatten MultiIndex columns if present (yfinance modern behavior)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Reset index so 'Date' becomes a regular column
        df = df.reset_index()

        # Add the ticker column
        df["Ticker"] = ticker

        all_data[ticker] = df

    # Combine all individual DataFrames into one large file
    if all_data:
        # combined_df = pd.concat(all_data, ignore_index=True)

        # # Reorder columns to put Ticker first
        # cols = ["Ticker"] + [
        #     col for col in combined_df.columns if col not in ["Ticker"]
        # ]
        # combined_df = combined_df[cols]

        # # Save to a single CSV file
        # output_file = "tech_stocks_15_years.csv"
        # combined_df.to_csv(output_file, index=False)
        # print(
        #     f"\nSuccess! Combined data saved to '{output_file}'. Total rows: {len(combined_df)}"
        # )
        return all_data
    else:
        print("No data was collected.")
        return None
