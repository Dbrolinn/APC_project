

import numpy as np
import pandas as pd

def triple_barrier_method(df, vertical_barrier=20, vol_multiplier=1.0):
    """
    Labels: -1 (Loss), 0 (Neutral), 1 (Profit)
    """
    labels = []
    
    # Iterate through the index (this is slow in python loops but fine for this project size)
    # For production, we would vectorise this.
    for i in range(len(df) - vertical_barrier):
        current_price = df['Close'].iloc[i]
        vol = df['Volatility'].iloc[i]
        
        # Dynamic Barriers based on volatility
        upper_barrier = current_price * (1 + vol * vol_multiplier)
        lower_barrier = current_price * (1 - vol * vol_multiplier)
        
        # Look forward
        future_prices = df['Close'].iloc[i+1 : i+1+vertical_barrier]
        
        # Find first touch
        # idxmax returns the index of the first True value
        hit_upper = (future_prices >= upper_barrier).idxmax() if (future_prices >= upper_barrier).any() else None
        hit_lower = (future_prices <= lower_barrier).idxmax() if (future_prices <= lower_barrier).any() else None
        
        label = 0 # Default to Neutral (Vertical Barrier)
        
        if hit_upper and hit_lower:
            if hit_upper < hit_lower:
                label = 1
            else:
                label = -1
        elif hit_upper:
            label = 1
        elif hit_lower:
            label = -1
            
        labels.append(label)
        
    # Align labels with original index
    labels_series = pd.Series(labels, index=df.index[:len(labels)])
    return labels_series
