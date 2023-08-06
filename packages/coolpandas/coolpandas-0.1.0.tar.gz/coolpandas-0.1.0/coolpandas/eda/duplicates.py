"""DataFrames cleaning module."""
import pandas as pd
from IPython.display import display


def duplicated_rows(
    data_frame: pd.DataFrame, display_summary: bool = True, drop: bool = False
) -> pd.DataFrame:
    """Get duplicated rows in a DataFrame and drop them if specified.
    Args:
        data_frame (pd.DataFrame): DataFrame to get duplicated rows.
        display_summary (bool, optional): Whether to display summary. Defaults to True.
        drop (bool, optional): Whether to drop duplicated rows. Defaults to True.
    Returns:
        pd.DataFrame: Duplicated rows.
    """
    duplicated_data_frame: pd.DataFrame = data_frame[data_frame.duplicated()]
    if display_summary:
        print(f"Number of duplicated rows: {duplicated_data_frame.shape[0]}")
        print("Head of duplicated rows DataFrame:")
        display(duplicated_data_frame.head())
    if drop:
        data_frame.drop_duplicates(inplace=True)
    if display_summary and drop:
        print("DataFrame shape after dropping duplicated rows:")
        print(data_frame.shape)
    return duplicated_data_frame


def duplicated_columns(
    data_frame: pd.DataFrame, display_summary: bool = True, drop: bool = False
) -> pd.DataFrame:
    """Get duplicated columns in a DataFrame and drop them if specified.
    Args:
        data_frame (pd.DataFrame): DataFrame to get duplicated columns.
        display_summary (bool, optional): Whether to display summary. Defaults to True.
        drop (bool, optional): Whether to drop duplicated columns. Defaults to True.
    Returns:
        pd.DataFrame: Duplicated columns.
    """
    duplicated_data_frame: pd.DataFrame = data_frame.T[data_frame.T.duplicated()].T
    if display_summary:
        print(f"Number of duplicated columns: {duplicated_data_frame.shape[1]}")
        print("Head of duplicated columns DataFrame:")
        display(duplicated_data_frame.head())
    if drop:
        data_frame.drop(columns=duplicated_data_frame.columns, inplace=True)
    if display_summary and drop:
        print("DataFrame shape after dropping duplicated columns:")
        print(data_frame.shape)
    return duplicated_data_frame
