import pandas as pd

def detect_smart_money(df):

    avg_volume = df['Volume'].rolling(20).mean()

    df['volume_spike'] = df['Volume'] > (2 * avg_volume)

    df['strong_move'] = (df['Close'] - df['Open']) / df['Open'] > 0.02

    df['smart_money_signal'] = df['volume_spike'] & df['strong_move']

    return df