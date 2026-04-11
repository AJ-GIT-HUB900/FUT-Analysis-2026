import pandas as pd

def calculate_moving_average(dataframe, window_size=3):
    # Sort by date just in case the CSV is out of order
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    dataframe = dataframe.sort_values(by='date')
    
    # Calculate the moving average
    dataframe[f'sma_{window_size}'] = dataframe['price'].rolling(window=window_size).mean()
    
    # Calculate percentage difference
    dataframe['diff_from_sma_%'] = ((dataframe['price'] - dataframe[f'sma_{window_size}']) / dataframe[f'sma_{window_size}']) * 100
    
    return dataframe

if __name__ == "__main__":
    print("Loading data from CSV...")
    
    # 1. READ THE CSV FILE!
    market_df = pd.read_csv('mbappe_prices.csv')
    
    # 2. Run the math
    result_df = calculate_moving_average(market_df, window_size=3)
    
    # 3. Print the results
    print("\nMarket Analysis for Mbappe:")
    print(result_df.dropna().to_string(index=False))