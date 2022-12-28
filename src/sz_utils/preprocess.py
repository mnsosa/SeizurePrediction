"""Functions for preprocessing data. It will be helpful for several models."""
import pandas as pd


def get_last_n_windows(
    df: pd.DataFrame, win_len: int, n_last: int
) -> list[pd.DataFrame]:
    """
    Return the last N windows of size win_len from the input DataFrame.

    :param df: Input DataFrame.
    :type df: pd.DataFrame
    :param win_len: Length of the window.
    :type win_len: int
    :param n_last: Number of windows to return.
    :type n_last: int
    :return: List of windows, each one represented as a DataFrame.
    :rtype: list[pd.DataFrame]

    Example:
    --------
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    get_last_n_windows(df, win_len=3, n_last=2)
    # Output: [   A
    #            8  9  10,
    #            5  6  7]
    """
    windows = []  # List to store the windows

    # Iterate over the range of indexes for the last N windows
    for i in range(n_last):
        # Compute the start and end index of the current window
        start = df.shape[0] - (i + 1) * win_len
        end = df.shape[0] - i * win_len

        # Append the current window to the list of windows
        windows.append(df.iloc[start:end])

    return windows

# %%
