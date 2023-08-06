#!/usr/bin/python

# vim: set expandtab ts=4 sw=4:

"""Test STFT Module."""

import unittest

import numpy as np
from scipy import signal


class TestSTFTAgainstScipy(unittest.TestCase):
    """Compare simple periodogram outputs against scipy."""

    def test_simple_periodogram_nperseg(self):
        """Ensure nperseg results are consistent."""
        from ..stft import periodogram

        # Run test 5 times
        for ii in range(5):
            xx = np.random.randn(4096,)
            f, pxx = signal.welch(xx, nperseg=2**(4+ii))
            f2, pxx2 = periodogram(xx, nperseg=2**(4+ii))

            assert(np.allclose(pxx, pxx2))

    def test_simple_periodogram_window_type(self):
        """Ensure window type results are consistent."""
        from ..stft import periodogram

        window_tests = ['hann', 'hamming', 'boxcar', 'tukey', 'blackman']

        for ii in range(5):
            xx = np.random.randn(4096,)
            f, pxx = signal.welch(xx, nperseg=128, window=window_tests[ii])
            f2, pxx2 = periodogram(xx, nperseg=128, window_type=window_tests[ii])

            assert(np.allclose(pxx, pxx2))

    def test_simple_periodogram_nfft(self):
        """Ensure nfft results are consistent."""
        from ..stft import periodogram

        for ii in range(5):
            xx = np.random.randn(4096,)
            f, pxx = signal.welch(xx, nfft=2**(ii+4), nperseg=16)
            f2, pxx2 = periodogram(xx, nfft=2**(ii+4), nperseg=16)

            assert(np.allclose(pxx, pxx2))

    def test_simple_periodogram_scaling(self):
        """Ensure scaling results are consistent."""
        from ..stft import periodogram

        scaling_tests = ['density', 'spectrum']

        for ii in range(len(scaling_tests)):
            xx = np.random.randn(4096,)
            f, pxx = signal.welch(xx, nperseg=128, scaling=scaling_tests[ii])
            f2, pxx2 = periodogram(xx, nperseg=128, scaling=scaling_tests[ii])

            assert(np.allclose(pxx, pxx2))
