""" Synthetic signals for testing purposes.

This module contains functions that generate synthetic signals for testing
purposes. The signals are generated using numpy.
"""
import numpy as np
from sz_utils import preprocess

# Generate a synthetic 1 Hz sine wave with a sampling frequency of 256 Hz
sampling_freq = 256
t = np.linspace(0, 1, sampling_freq)
signal = np.sin(2 * np.pi * 1 * t)

# Decompose the signal into frequency bands
alfa_amplitudes, beta_amplitudes, delta_amplitudes, gamma_amplitudes = preprocess.decompose_into_bands(signal, sampling_freq)

# print alfa_

