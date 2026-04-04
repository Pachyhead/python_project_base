import pandas as pd

def print_value_ratios(dataframe: pd.DataFrame, column_name: str):
    """
    1. Count the occurrences of each value.
    2. Set normalize to True to get the ratio.
    """
    ratios = dataframe[column_name].value_counts(normalize=True)
    
    print(f"--- Ratios for '{column_name}' ---")
    print(ratios)

def print_value_counts(dataframe: pd.DataFrame, column_name: str):
    """
    1. Count the occurrences of each value.
    2. Set normalize to True to get the ratio.
    """
    counts = dataframe[column_name].value_counts()
    
    print(f"--- Ratios for '{column_name}' ---")
    print(counts)