def create_lagged_features(df, target='T (degC)', n_lags=144):
    for lag in range(1, n_lags + 1):
        df[f'{target}_lag_{lag}'] = df[target].shift(lag)
    df = df.dropna().reset_index(drop=True)
    return df
