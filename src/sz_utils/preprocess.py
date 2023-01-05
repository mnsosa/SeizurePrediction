"""Functions for preprocessing data. 

Data cleaning, feature engineering, etc.

It will be helpful for several models.
"""
import pandas as pd
import numpy as np
from scipy import fftpack


def get_frequencies_amplitudes(
    signal: np.ndarray, sampling_freq: float
) -> tuple[list, list]:
    """Get the frequencies and amplitudes of the signal.

    :param signal: The signal to decompose.
    :type signal: np.ndarray
    :param sampling_freq: The sampling frequency of the signal, in Hz.
    :type sampling_freq: float
    :return: A tuple containing two lists with the frequencies and amplitudes of the signal.
    :rtype: tuple[list, list]
    """

    # Perform the Fast Fourier Transform on the signal
    fft = fftpack.fft(signal)

    # Calculate the range of frequencies
    frequencies = fftpack.fftfreq(len(fft)) * sampling_freq  # type: ignore

    # Get the absolute value of each frequency component
    amplitudes = np.abs(fft)

    return frequencies, amplitudes


def decompose_into_bands(
    signal: np.ndarray, sampling_freq: float
) -> tuple[list, list, list, list]:
    """
    Decompose the given signal into four bands of frequency: alpha, beta, delta and gamma.

    :param signal: The signal to decompose.
    :type signal: np.ndarray
    :param sampling_freq: The sampling frequency of the signal, in Hz.
    :type sampling_freq: float
    :return: A tuple containing four lists with the amplitudes of the frequency bands.
    :rtype: tuple[list, list, list, list]
    """

    frequencies, amplitudes = get_frequencies_amplitudes(signal, sampling_freq)

    # Initialize lists to store the amplitudes of each frequency band
    alfa_amplitudes = []
    beta_amplitudes = []
    delta_amplitudes = []
    gamma_amplitudes = []

    # Iterate over frequencies and amplitudes and store the amplitudes in the corresponding lists
    for frequency, amplitude in zip(frequencies, amplitudes):
        if frequency >= 8 and frequency <= 13:
            alfa_amplitudes.append(amplitude)
        elif frequency >= 13 and frequency <= 30:
            beta_amplitudes.append(amplitude)
        elif frequency >= 0.5 and frequency <= 4:
            delta_amplitudes.append(amplitude)
        elif frequency >= 30 and frequency <= 100:
            gamma_amplitudes.append(amplitude)

    return alfa_amplitudes, beta_amplitudes, delta_amplitudes, gamma_amplitudes


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


def assign_window_values(windows) -> list[int]:
    """
    Assigns a label to each window in the list of windows based on the number of samples remaining
    from the middle of the window to the seizure.

    The label for each window is calculated as follows: window length * (0.5 + window index)

    :param windows: List of windows.
    :type windows: list[pd.DataFrame]
    :return: List of labels assigned to each window.
    :rtype: list[int]
    """
    window_values = []
    for i, window in enumerate(windows):
        window_value = int(len(window) * (0.5 + i))
        window_values.append(window_value)
    return window_values
