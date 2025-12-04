
import pandas as pd

import numpy as np


def calculate_rsi(series, window=14):

    delta = series.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()

    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss

    return 100 - (100 / (1 + rs))


def calculate_bollinger_bandwidth(series, window=20, num_std=2):

    ma = series.rolling(window=window).mean()

    std = series.rolling(window=window).std()

    upper = ma + (std * num_std)

    lower = ma - (std * num_std)

    return (upper - lower) / ma


def generate_features(df):

    """

    Generates technical indicators.

    """

    df = df.copy()

    

    # 1. RSI (Velocity)

    df['RSI'] = calculate_rsi(df['Close'])

    

    # 2. MACD (Acceleration)

    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()

    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()

    df['MACD'] = ema_12 - ema_26

    

    # 3. Bollinger Bandwidth (Potential Energy)

    df['BBW'] = calculate_bollinger_bandwidth(df['Close'])

    

    # 4. Volatility (for Labeling barriers later)

    df['Volatility'] = df['Close'].pct_change().rolling(window=20).std()

    

    return df.dropna()
