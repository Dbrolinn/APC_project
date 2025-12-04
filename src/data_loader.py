import yfinance as yf
import pandas as pd

def download_data(ticker="BTC-USD", start="2020-01-01", end="2024-01-01", interval="1h"):
    """
    Downloads crypto data from Yahoo Finance.
    """
    print(f"Downloading {ticker} data...")
    df = yf.download(ticker, start=start, end=end, interval=interval)
    
    # Flatten multi-index columns if they exist (yfinance quirk)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    print(f"Downloaded {len(df)} rows.")
    return df
