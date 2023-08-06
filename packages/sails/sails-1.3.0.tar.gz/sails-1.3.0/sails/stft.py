#!/usr/bin/python

# vim: set expandtab ts=4 sw=4:

"""
Functions for computing power spectra based on windowed Fast Fourier Transforms.

The module contains four types of function.

* worker functions which perform detailed computation - these functions do not
necessarily have globally sensible or adaptive defaults and some additional
processing may be required to get a full spectrum from them. For example,
windows and scaling factors may need to be precomputed.
* config function which set, check and provide parameter values
* helper functions isolate code from worker and config functions and are typically _private
* user functions which provide a top-level interface to the module

The user functions are intended for day to day use, though the worker functions
can be called directly if needed.

User functions:
    periodogram
    sw_periodogram
    multitaper
    sw_multitaper
    glm_periodogram

Config classes:
    STFTConfig
    PeriodogramConfig
    MultiTaperConfig
    GLMPeriodogramConfig

Worker functions:
    apply_sliding_window
    compute_fft
    compute_stft
    compute_multitaper_stft

"""

import logging
import typing
import warnings
from dataclasses import dataclass
from functools import wraps

import numpy as np
from scipy import fft as sp_fft
from scipy import stats
from scipy.signal import signaltools
from scipy.signal.windows import dpss

try:
    from scipy.signal.spectral import _triage_segments
except ImportError:
    # scipy.signal was refactored in v1.8.0
    from scipy.signal._spectral_py import _triage_segments

# Will configure a proper logger later
logging.basicConfig(level=logging.DEBUG)


# Decorator for setting and reverting logging level. Top level functions should
# specify verbose but within internal operations we ALWAYS set verbose=None to
# preserve current level. Only top-level user called function should have a
# specification.
def set_verbose(func):
    """Add option to change logging level for single function calls."""
    # This is the actual decorator
    @wraps(func)
    def inner_verbose(*args, **kwargs):

        # Change level if requested
        if ('verbose' in kwargs) and (kwargs['verbose'] is not None):
            if kwargs['verbose'].upper() in ['DEBUG', 'INFO', 'WARNING', 'CRITICAL']:
                logging.getLogger().setLevel(getattr(logging, kwargs['verbose']))

                if kwargs['verbose'] == 'DEBUG':
                    formatter = logging.Formatter('%(asctime)-s - %(levelname)-8s %(funcName)30s : %(message)s')
                    formatter.datefmt = '%H:%M:%S'
                else:
                    formatter = logging.Formatter('%(funcName)30s - %(message)s')
                logging.getLogger().handlers[0].setFormatter(formatter)
            else:
                raise ValueError("Logger level '{}' not recognised".format(kwargs['verbose']))

        # Call function itself
        func_output = func(*args, **kwargs)

        # If we changed anything, change it back - otherwise preserve current level
        if ('verbose' in kwargs) and (kwargs['verbose'] is not None):
            logging.getLogger().setLevel(logging.WARNING)

        return func_output
    return inner_verbose

# ------------------------------------------------------------------
# Worker Functions
#
# These functions are stand-alone data processors which are usable on their own
# Inputs are not sanity checked and documentation may point elsewhere but these
# are fast and flexible for expert users.
#
# Most users will likely interact with these via the high level and config functions.


@set_verbose
def apply_sliding_window(x, nperseg, nstep, window=None, detrend_func=None, padded=False, verbose=None):
    """Apply a delay-embedding to the last axis of an array.

    Create a windowed versions of a dataset with options for specifying
    padding, detrendingand windowing operations.

    Parameters
    ----------
    x : ndarray
        Array of data
    nperseg : int
        Length of delay embedding segment
    nstep : int
        Length of step between successive windows
    window : ndarray
        Vector containing windowing function to be applied (default = None)
    detrend_func : function
        Function applying detrending to final axis of an array (default = None)
    padded : bool
        Flag indicating whether to pad datast to integer number of windows (default = None)

    Returns
    -------
    ndarray
        Data array with delay embedding applied

    Notes
    -----
    Strongly inspired by scipy.signal.spectral._fft_helper with the FFT
    computation separate out.

    """
    # pad to make the vector length an integer number of windows
    msg = 'Applying sliding windows of nperseg : {0} nstep : {1}'
    logging.info(msg.format(nperseg, nstep))

    if padded:
        nadd = (-(x.shape[-1]-nperseg) % nstep) % nperseg
        zeros_shape = list(x.shape[:-1]) + [nadd]
        y = np.concatenate((x, np.zeros(zeros_shape)), axis=-1)
    else:
        y = x

    # Strided array
    # https://github.com/scipy/scip/y/blob/v1.5.1/scipy/signal/spectral.py#L1896
    noverlap = nperseg-nstep
    step = nperseg - noverlap
    shape = y.shape[:-1]+((y.shape[-1]-noverlap)//step, nperseg)
    strides = y.strides[:-1]+(step*y.strides[-1], y.strides[-1])
    y_window = np.lib.stride_tricks.as_strided(y, shape=shape, strides=strides)

    logging.info('Created {0} windows of length {1}'.format(y_window.shape[-2], y_window.shape[-1]))
    logging.debug('windowed data shape : {0}'.format(y_window.shape))

    if detrend_func is not None:
        logging.debug('applying detrending {0} '.format(detrend_func))
        y_window = detrend_func(y_window)

    if window is not None:
        # Apply windowing
        logging.debug('applying windowing {0} '.format(window.sum()))
        y_window = window * y_window

    msg = 'output shape : {0}'
    logging.debug(msg.format(y_window.shape))

    return y_window


@set_verbose
def compute_fft(x, nfft=256, axis=-1,
                side='onesided', mode='psd', scale=1.0,
                fs=1.0, fmin=-0.5, fmax=0.5, verbose=None):
    """Compute, trim and post-process an FFT on last dimension of input array.

    Parameters
    ----------
    x : ndarray
        Array of data
    nfft : int
        Length of the FFT to use (Default value = 256)
    axis : int
        Axis along which the FFT is computed across the input array `x` (Default value = -1)
    side : {'onesided', 'twosided'}
        Whether to return a one-sided or two-sided spectrum (Default value = 'onesided')
    mode : {'psd', 'magnitude', 'angle', 'phase', 'complex'}
        Which type of spectrum to return (Default value = 'psd')
    scale : float
        Scaling factor to be applied to FFT result. Typically defined by
        `_set_scaling` via the config options (Default value = 1.0)
    fs : float
        Sampling frequency of the input array `x` (Default value = 1.0)
    fmin : float
        Minimum frequency value in the returned spectrum. This is defined in Hz
        and is dependent on the value of `fs` (Default value = -0.5)
    fmax : float
        Maximum frequency value in the returned spectrum. This is defined in Hz
        and is dependent on the value of `fs` (Default value = 0.5)

    Returns
    -------
    f : ndarray
        Array of sample frequencies.
    spec : ndarray
        FFT spectrum of x.

    """
    # Compute FFT
    if side == 'twosided':
        func = sp_fft.fft
    else:
        x = x.real
        func = sp_fft.rfft
    logging.info('Computing {0}-point {1} FFT with {2}'.format(nfft, side, func))
    result = func(x, nfft)
    logging.debug('fft output shape {0}'.format(result.shape))

    # Apply spectrum mode selection
    result = _proc_spectrum_mode(result, mode, axis=axis)

    # Apply scaling
    result = _proc_spectrum_scaling(result, scale, side, mode, nfft)

    # Get frequency values
    freqvals = _set_freqvalues(nfft, fs, side)
    # Trim frequency range to specified limits
    logging.info('Trimming freq axis to range {0} - {1}'.format(fmin, fmax))
    fidx = (freqvals >= fmin) & \
           (freqvals <= fmax)
    result = result[..., fidx]
    freqs = freqvals[fidx]
    logging.debug('fft trimmed output shape {0}'.format(result.shape))

    return freqs, result


@set_verbose
def compute_stft(x, fs=1.0, fmin=0, fmax=0.5, axis=-1,
                 # window kwargs
                 nperseg=256, nstep=256, window=None, detrend_func=None, padded=False,
                 # FFT kwargs
                 nfft=256, side='onesided', mode='psd', scale=1.0,
                 # misc
                 output_axis='auto', verbose=None):
    """Compute a short-time Fourier transform to a dataset.

    Parameters
    ----------
    x : ndarray
        Array of data
    fs : float
        sampling frequency of the data (default = 1.0)
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    axis : int, optional
        Axis along which the FFTs are computed; the default is over the
        last axis (i.e. ``axis=-1``).
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    nstep : int, optional
        Number of points to step forward between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    window : tuple or array_like, optional
        Vector containing Desired window to use. Defaults to a `None` window.
    detrend_func : function or `None`, optional
        Specifies how to detrend each segment. Either a function that takes a
        segment and returns a detrended segment or `None` for no detrending.
        Defaults to 'constant'.
    padded : bool, optional
        Specifies whether the input signal is zero-padded at the end to
        make the signal fit exactly into an integer number of window
        segments, so that all of the signal is included in the output.
        Defaults to `False`. Padding occurs after boundary extension, if
        `boundary` is not `None`, and `padded` is `True`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    side : {'onesided', 'twosided'}, optional
        Indicate whether to return a one-sided spectrum or a two-sided
        spectrum. Defaults to `onesided`.
    mode : {'psd', 'magnitude', 'angle', 'phase', 'complex'}, optional
        Defines what kind of return values are expected. Defaults to
        'psd'.
    scale : float
        Scaling factor to be applied to FFT result. Typically defined by
        `_set_scaling` via the config options (Default value = 1.0)
    boundary : str or None, optional
        Specifies whether the input signal is extended at both ends, and
        how to generate the new values, in order to center the first
        windowed segment on the first input point. This has the benefit
        of enabling reconstruction of the first input point when the
        employed window function starts at zero. Valid options are
        ``['even', 'odd', 'constant', 'zeros', None]``. Defaults to
        `None`.
    output_axis : {'auto', 'time_first'}
        Flag indicating where to roll the time and frequencies dimensions to in
        output array. 'auto' will return the transformed dimensions back the
        position of the transformed input, 'glm' will roll the time windows to (Default value = 'auto')

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.

    Notes
    -----
    Initially adapted from scipy.signal.spectral._spectral_helper.

    """
    # ---- Work start here
    if axis == -1:
        axis = x.ndim-1
    x = _proc_roll_input(x, axis=axis)

    # window inputs
    y = apply_sliding_window(x, nperseg, nstep, detrend_func=detrend_func, window=window, padded=padded)

    # Run actual FFT
    freqs, result = compute_fft(y, nfft=nfft, axis=axis, side=side, mode=mode,
                                scale=scale, fs=fs, fmin=fmin, fmax=fmax)

    # Create time window vector
    noverlap = nperseg - nstep
    time = np.arange(nperseg/2, x.shape[-1] - nperseg/2 + 1,
                     nperseg - noverlap)/float(fs)

    # Final two axes are now [..., time x freq]
    result = _proc_unroll_output(result, axis, output_axis=output_axis)

    return freqs, time, result


@set_verbose
def compute_multitaper_stft(x, num_tapers='auto', freq_resolution=1, time_bandwidth=5,
                            apply_tapers='broadcast',
                            # Data kwargs
                            fs=1.0, fmin=0, fmax=0.5, axis=-1,
                            # window kwargs
                            nperseg=256, nstep=256, window=None, detrend_func=None, padded=False,
                            # FFT kwargs
                            nfft=256, side='onesided', mode='psd', scale=1.0,
                            # misc
                            output_axis='auto', verbose=None):
    """Compute a multi-tapered short time fourier transform.

    Parameters
    ----------
    x : ndarray
        Array of data
    num_tapers : {int, 'auto'}
        The number of tapers to use if set to an integer value, if set to
        `'auto'` then the number of tapers is automatically computed from
        `freq_resolution` and `time_bandwidth` (Default value = 'auto')
    freq_resolution : int
        Required frequency resolution of the tapers used if `num_tapers` is set
        to `auto` (Default value = 1)
    time_bandwidth : int
        Required time bandwidth value of the tapers used if `num_tapers` is set
        to `auto` (Default value = 5)
    fs : float
        sampling frequency of the data (default = 1.0)
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    axis : int, optional
        Axis along which the FFTs are computed; the default is over the
        last axis (i.e. ``axis=-1``).
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    nstep : int, optional
        Number of points to step forward between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    window : tuple or array_like, optional
        Vector containing Desired window to use. Defaults to a `None` window.
    detrend_func : function or `None`, optional
        Specifies how to detrend each segment. Either a function that takes a
        segment and returns a detrended segment or `None` for no detrending.
        Defaults to 'constant'.
    padded : bool, optional
        Specifies whether the input signal is zero-padded at the end to
        make the signal fit exactly into an integer number of window
        segments, so that all of the signal is included in the output.
        Defaults to `False`. Padding occurs after boundary extension, if
        `boundary` is not `None`, and `padded` is `True`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    side : {'onesided', 'twosided'}, optional
        Indicate whether to return a one-sided spectrum or a two-sided
        spectrum. Defaults to `onesided`.
    mode : {'psd', 'magnitude', 'angle', 'phase', 'complex'}, optional
        Defines what kind of return values are expected. Defaults to
        'psd'.
    scale : float
        Scaling factor to be applied to FFT result. Typically defined by
        `_set_scaling` via the config options (Default value = 1.0)
    boundary : str or None, optional
        Specifies whether the input signal is extended at both ends, and
        how to generate the new values, in order to center the first
        windowed segment on the first input point. This has the benefit
        of enabling reconstruction of the first input point when the
        employed window function starts at zero. Valid options are
        ``['even', 'odd', 'constant', 'zeros', None]``. Defaults to
        `None`.
    output_axis : {'auto', 'time_first'}
        Flag indicating where to roll the time and frequencies dimensions to in
        output array. 'auto' will return the transformed dimensions back the
        position of the transformed input, 'glm' will roll the time windows to (Default value = 'auto')

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.

    """
    if num_tapers == 'auto':
        seconds_perseg = nperseg / fs
        time_half_bandwidth = int(seconds_perseg * freq_resolution / 2)
        num_tapers = 2 * time_half_bandwidth - 1

        msg = 'freq_resolution : {0} time_bandwidth : {1} time_half_bandwidth: {2}'
        logging.debug(msg.format(freq_resolution, time_bandwidth, time_half_bandwidth))
        logging.info('Using auto-computed number of tapers - {0}'.format(num_tapers))
    else:
        logging.info('Using user-specified number of tapers - {0}'.format(num_tapers))

    tapers, ratios = dpss(nperseg, time_bandwidth, num_tapers, return_ratios=True)
    taper_weights = np.ones((num_tapers,)) / num_tapers

    # ---- Work start here
    if axis == -1:
        axis = x.ndim-1
    x = _proc_roll_input(x, axis=axis)

    # delay embedding - don't apply normal window function... will apply tapers next
    y = apply_sliding_window(x, nperseg, nstep,
                             detrend_func=detrend_func,
                             window=None, padded=padded)

    if apply_tapers == 'broadcast':
        # Apply tapers - via broadcasting to avoid loops
        to_shape = np.r_[np.ones((len(y.shape)-1),), num_tapers, nperseg].astype(int)
        z = y[..., np.newaxis, :] * np.broadcast_to(tapers, to_shape)
        logging.debug('tapered data shape {0}'.format(z.shape))

        # Run actual FFT
        freqs, result = compute_fft(z, nfft=nfft, axis=-1, side=side, mode=mode,
                                    scale=scale, fs=fs, fmin=fmin, fmax=fmax)
        logging.debug('tapered and fftd data shape {0}'.format(result.shape))

        # Average over tapers - could be high level option? mean or median?
        result = np.average(result, weights=taper_weights, axis=-2)

    elif apply_tapers == 'loop':
        # Apply tapers in a loop - slower but uses much less RAM
        to_shape = np.r_[np.ones((len(y.shape)-1),), nperseg].astype(int)
        for ii in range(num_tapers):
            logging.info('running taper: {0}'.format(ii))
            z = y * np.broadcast_to(tapers[ii, :], to_shape)
            # Run actual FFT
            freqs, taper_result = compute_fft(z, nfft=nfft, axis=-1, side=side, mode=mode,
                                              scale=scale, fs=fs, fmin=fmin, fmax=fmax)
            logging.debug('tapered and fftd data shape {0}'.format(taper_result.shape))

            # Run an incremental average so we don't have to store anything
            # https://math.stackexchange.com/questions/106700/incremental-averaging/1836447
            if ii == 0:
                result = taper_result
            else:
                result = result + (taper_result - result) / (ii + 1)
    else:
        msg = "'apply_tapers' option '{0}' not recognised. Use one of 'broadcast' or 'loop''"
        raise ValueError(msg.format(apply_tapers))

    # Periodogram Scaling
    result = result / fs

    # Create time window vector
    noverlap = nperseg - nstep
    time = np.arange(nperseg/2, x.shape[-1] - nperseg/2 + 1,
                     nperseg - noverlap)/float(fs)

    # Final two axes are now [..., time x freq] - return them to requested position
    result = _proc_unroll_output(result, axis, output_axis=output_axis)

    return freqs, time, result


def compute_spectral_matrix_fft(psd):
    """Compute a spectral matrix from a periodogram."""
    # psd should be [channels x freq] complex for now
    S = np.zeros((psd.shape[0], psd.shape[0], psd.shape[1]), dtype=complex)

    for ii in range(psd.shape[1]):
        S[:, :, ii] = np.dot(psd[:, ii, np.newaxis], psd[np.newaxis, :, ii].conj())

    return S


# Helpers - private functions assisting low-level processors

def _proc_roll_input(x, axis=-1):
    """Move axis to be transformed to final position.

    Parameters
    ----------
    x : ndarray
        array of numeric data values
    axis : int
        Axis to be rolled into final position (Default value = -1)

    Returns
    -------
    x : ndarray
        A view of x with the specified axes rolled to final position

    """
    logging.debug('Rolling input axis position {0} to end'.format(axis))
    logging.debug('Pre-rolled shape - {0}'.format(x.shape))
    if axis != -1:
        x = np.rollaxis(x, axis, len(x.shape))
    logging.debug('Post-rolled shape - {0}'.format(x.shape))
    return x


def _proc_unroll_output(result, axis, output_axis='auto'):
    """Move time and frequency dimensions to user specified position.

    Parameters
    ----------
    result : ndarray
        array of numeric data values, typically an output from `compute_stft`
    axis : int
        Axis in original dataset which has been short-time fourier transformed.
    output_axis : {'auto', 'time_first'}
        If `auto`, then move both time and frequency axes back to original
        position specified by `axis`. If `time_first` then move the time axis
        to first position and frequency axis back to original position (Default
        value = 'auto')

    Returns
    -------
    result : ndarray
        A view of the input array with the axis rolled to specified positions.

    Notes
    -----
    The `time_first` option is used to simplify the subsequent temporal
    averaging of standard periodograms and the computation of GLM-periodograms
    which require the temporal dimension in the first position.

    """
    logging.debug('Rolling output axis {0} to position {1}'.format(axis, output_axis))
    logging.debug('Pre-rolled shape {0}'.format(result.shape))
    if output_axis == 'auto':
        # Return time and freq back to original position
        result = np.rollaxis(result, -2, axis)
        result = np.rollaxis(result, -1, axis+1)
    elif output_axis == 'time_first':
        # Put time at front and freq in original position
        result = np.rollaxis(result, -2, 0)
        result = np.rollaxis(result, -1, axis+1)

    logging.debug('Post-rolled shape {0}'.format(result.shape))
    return result


def _proc_spectrum_mode(pxx, mode, axis=-1):
    """Apply specified transformation to STFT result.

    Parameters
    ----------
    pxx : ndarray
        Array containing a complex valued Fourier transform result.
    mode : {'psd', 'magnitude', 'angle', 'phase', 'complex'}, optional
        Defines what kind of return values are expected. Defaults to 'psd'.
    axis : int
        Axis containing the frequency dimension, required for the `phase` mode
        (Default value = -1)

    Returns
    -------
    pxx : ndarray
        Array containing the transformed power spectrum

    """
    logging.debug('computing {0} spectrum'.format(mode))
    if mode == 'magnitude':
        pxx = np.abs(pxx)
    elif mode == 'psd':
        pxx = (np.conjugate(pxx) * pxx).real
    elif mode in ['angle', 'phase']:
        pxx = np.angle(pxx)
        if mode == 'phase':
            # pxx has one additional dimension for time strides
            if axis < 0:
                axis -= 1
            pxx = np.unwrap(pxx, axis=axis)
    elif mode == 'complex':
        pass
    return pxx


def _proc_spectrum_scaling(pxx, scale, side, mode, nfft):
    """Apply specified unit scaling to STFT output.

    Need to ignore DC and Nyquist frequencies to ensure that overall power is
    consistent with time-dimension.

    Parameters
    ----------
    pxx : ndarray
        Array containing a complex valued Fourier transform result.
    scale : float
        Scaling factor to be applied to FFT result. Typically defined by
        `_set_scaling` via the config options (Default value = 1.0)
    side :
        Indicate whether to return a one-sided spectrum or a two-sided
        spectrum. Defaults to `onesided`.
    mode : {'psd', 'magnitude', 'angle', 'phase', 'complex'}, optional
        Defines what kind of return values are expected. Defaults to 'psd'.
    nfft : int
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.

    Returns
    -------
    pxx : ndarray
        Scaled version of input power spectrum

    """
    logging.debug('Applying scaling factor {0}'.format(scale))

    pxx *= scale

    # Need to handle first and last points differently in onesided and twosided modes
    if side == 'onesided' and mode == 'psd':
        if nfft % 2:
            pxx[..., 1:] *= 2
        else:
            # Last point is unpaired Nyquist freq point, don't double
            pxx[..., 1:-1] *= 2
    return pxx


# ------------------------------------------------------------------
# Config Functions
#
# These functions parse inputs, set defaults and return sets of configured
# options.


def _set_freqvalues(nfft, fs, sides):
    """Set frequency values for FFT.

    Parameters
    ----------
    nfft : int
        Length  of FFT to compute
    fs : float
        Sampling rate of the data
    sides : {'twosided', 'twosided'}
        Indication of whether a 1 or 2 sided FFT is being computed

    Returns
    -------
    ndarray
        Vector of frequency values

    """
    if sides == 'twosided':
        freqs = sp_fft.fftfreq(nfft, 1/fs)
    elif sides == 'onesided':
        freqs = sp_fft.rfftfreq(nfft, 1/fs)

    return freqs


def _set_onesided(return_onesided, input_complex):
    """Set flag indicating whether FFT will be one- or two-sided.

    Parameters
    ----------
    return_onesided : bool
        Flag indicating whether one-sided FFT is preferred
    input_complex : bool
        Flag indicating whether input array is complex

    Returns
    -------
    str
        One of 'onesided' or 'twosided'

    """
    if return_onesided:
        if input_complex:
            sides = 'twosided'
            warnings.warn('Input data is complex, switching to return_onesided=False')
        else:
            sides = 'onesided'
    else:
        sides = 'twosided'

    return sides


def _set_nfft(nfft, nperseg):
    """Set FFT length.

    Parameters
    ----------
    nfft : int
        Desired FFT length
    nperseg : int
        Selected segment length for STFT

    Returns
    -------
    int
        Selected length of FFT

    """
    if nfft is None:
        nfft = nperseg
    elif nfft < nperseg:
        raise ValueError('nfft must be greater than or equal to nperseg.')
    else:
        nfft = int(nfft)
    return nfft


def _set_noverlap(noverlap, nperseg):
    """Set length over overlap between successive windows.

    Parameters
    ----------
    noverlap : int
        Desired number of overlapping samples between successive windows.
    nperseg : int
        Window length

    Returns
    -------
    int
        Number of overlapping samples between successive windows.

    """
    if noverlap is None:
        noverlap = nperseg//2
    else:
        noverlap = int(noverlap)
    if noverlap >= nperseg:
        raise ValueError('noverlap must be less than nperseg.')
    return noverlap


def _set_scaling(scaling, fs, win):
    """Set scaling to be applied to FFT output.

    Parameters
    ----------
    scaling : {'density', 'spectrum', None}
        Selected type of scaling
    fs : float
        Sampling rate of the data
    win : ndarray
        Windowing function

    Returns
    -------
    float
        Scaling factor to apply to FFT result

    """
    logging.debug("setting scaling '{0}' {1}".format(scaling, fs))
    if scaling == 'density':
        scale = 1.0 / (fs * (win*win).sum())
    elif scaling == 'spectrum':
        scale = 1.0 / win.sum()**2
    elif scaling is None:
        scale = 1.0
    else:
        raise ValueError('Unknown scaling: %r' % scaling)
    return scale


def _set_heinzel_scaling(fs, win, input_length):
    """Compute FFT scaling factors with Heinzel method.

    https://holometer.fnal.gov/GH_FFT.pdf - section 9

    EXPERIMENTAL - NOT YET PLUGGED IN.

    Parameters
    ----------
    fs : float
        Sampling rate of the data
    win : ndarray
        Windowing function
    input_length : int
        Length of input data

    Returns
    -------
    nenbw : float
        normalised effective noise bandwidth
    enbw : float
        effective noise bandwidth

    """
    s1 = win.sum()
    s2 = (win*win).sum()

    nenbw = len(win) * (s2 / s1**2)
    enbw = fs * (s2 / s1**2)

    return nenbw, enbw


def _set_detrend(detrend, axis):
    """Set a detrending function to be applied to STFT windows prior to FFT.

    Parameters
    ----------
    detrend : {False, str, func}
        One of either:
        * False or None - Detrend function does nothing

        * str - detrend function defined by signaltools.detrend with type=detrend.

        * func - specified detrend function is returned

    axis : int
        Axis to apply detrending to.

    Returns
    -------
    func
        Detrending function

    """
    # Handle detrending and window functions
    if not detrend:
        def detrend_func(d):
            return d
    elif not hasattr(detrend, '__call__'):
        def detrend_func(d):
            return signaltools.detrend(d, type=detrend, axis=-1)
    elif axis != -1:
        # Wrap this function so that it receives a shape that it could
        # reasonably expect to receive.
        def detrend_func(d):
            d = np.rollaxis(d, -1, axis)
            d = detrend(d)
            return np.rollaxis(d, axis, len(d.shape))
    else:
        detrend_func = detrend
    return detrend_func


def _set_mode(mode):
    """Set output mode for FFT result.

    Parameters
    ----------
    mode : {'psd', 'complex', 'magnitude', 'angle', 'phase'}
        str indicating which type of spectrum is to be computed

    Raises
    ------
    ValueError
        If non-valid mode is specified

    """
    modelist = ['psd', 'complex', 'magnitude', 'angle', 'phase']
    if mode not in modelist:
        raise ValueError("Invalid value ('{}') for mode, must be one of {}"
                         .format(mode, modelist))


def _set_frange(fmin, fmax, fs):
    """Set range of frequenecy values to be returned from FFT result.

    Parameters
    ----------
    fmin : {float, None}
        Smallest frequency in desired range (left hand boundary)
    fmax : {float, None}
        Largest frequency in desired range (right hand boundary)
    fs : float
        Sampling rate of the data

    Returns
    -------
    float, float
        fmin and fmax

    """
    if fmin is None:
        fmin = 0
    if fmax is None:
        fmax = fs/2

    return fmin, fmax


@dataclass
class STFTConfig:
    """Configuration options for a Short Time Fourier Transform.

    This sets user options and sensible defaults for an STFT to be applied to a
    specific dataset. It may not generalise to datasets of different lengths,
    sampling rates etc.

    """

    # Data specific args
    input_len: int
    axis: int = -1
    input_complex: bool = False
    # General FFT args
    fs: float = 1.0
    window_type: str = 'hann'
    nperseg: int = None
    noverlap: int = None
    nfft: int = None
    detrend: typing.Union[typing.Callable, str] = 'constant'
    return_onesided: bool = True
    scaling: str = 'density'
    mode: str = 'psd'
    boundary: str = None  # Not currently used...
    padded = bool = False
    fmin: float = None
    fmax: float = None
    output_axis: typing.Union[int, str] = 'auto'

    def __post_init__(self):
        """Set user picks and fill rest with sensible defaults."""
        if self.window_type is None:
            # Set a rectangular boxcar of 1s as the window if None is requested
            # - keeps following code cleaner.
            self.window_type = 'boxcar'
        self.window, self.nperseg = _triage_segments(self.window_type, self.nperseg, input_length=self.input_len)
        self.nfft = _set_nfft(self.nfft, self.nperseg)
        self.noverlap = _set_noverlap(self.noverlap, self.nperseg)
        self.nstep = self.nperseg - self.noverlap
        self.nwindows = np.fix(self.input_len/self.nstep - 1).astype(int)
        self.scale = _set_scaling(self.scaling, self.fs, self.window)
        self.detrend_func = _set_detrend(self.detrend, axis=self.axis)
        self.side = _set_onesided(self.return_onesided, self.input_complex)
        self.freqvals = _set_freqvalues(self.nfft, self.fs, self.side)
        self.fmin, self.fmax = _set_frange(self.fmin, self.fmax, self.fs)
        _set_mode(self.mode)
        logging.debug(self)

    @property
    def stft_args(self):
        """Get keyword arguments for a call to compute_stft."""
        args = {}
        for key in ['fs', 'nperseg', 'nstep', 'nfft', 'detrend_func',
                    'side', 'scale', 'axis', 'mode', 'window',
                    'padded', 'fmin', 'fmax', 'output_axis']:
            args[key] = getattr(self, key)
        return args

    @property
    def sliding_window_args(self):
        """Get keyword arguments for a call to apply_sliding_window."""
        args = {}
        for key in ['nperseg', 'nstep', 'detrend_func', 'window', 'padded']:
            args[key] = getattr(self, key)
        return args

    @property
    def fft_args(self):
        """Get keyword arguments for a call to compute_fft."""
        args = {}
        for key in ['nfft', 'axis', 'side', 'mode', 'scale', 'fs', 'fmin', 'fmax']:
            args[key] = getattr(self, key)
        return args


@dataclass
class PeriodogramConfig(STFTConfig):
    """Configuration options for a Periodogram.

    This inhrits from STFTConfig and includes extra periodogram specific arguments:
        'average'

    This sets user options and sensible defaults for Periodogram to be applied
    to a specific dataset. It may not generalise to datasets of different
    lengths, sampling rates etc.

    """

    average: str = 'mean'

    def __post_init__(self):
        """Set user picks and fill rest with sensible defaults."""
        super().__post_init__()


@dataclass
class GLMPeriodogramConfig(STFTConfig):
    """Configuration options for a GLM Periodogram.

    This inhrits from STFTConfig and includes extra periodogram specific arguments:
        'covariates'
        'confounds'
        'fit_method'
        'fit_constant'

    This sets user options and sensible defaults for Periodogram to be applied
    to a specific dataset. It may not generalise to datasets of different
    lengths, sampling rates etc.

    """

    covariates: dict = None
    confounds: dict = None
    fit_method: str = 'pinv'
    fit_constant: bool = True

    def __post_init__(self):
        """Set user picks and fill rest with sensible defaults."""
        super().__post_init__()


@dataclass
class MultiTaperConfig(STFTConfig):
    """Configuration options for a GLM Periodogram.

    This inhrits from STFTConfig and includes extra periodogram specific arguments:
        'average'
        'time_bandwidth'
        'num_tapers'
        'freq_resolution'
        'apply_tapers'

    This sets user options and sensible defaults for Periodogram to be applied
    to a specific dataset. It may not generalise to datasets of different
    lengths, sampling rates etc.

    """

    average: str = 'mean'
    time_bandwidth: int = 3
    num_tapers: typing.Union[str, int] = 'auto'
    freq_resolution: int = 1
    apply_tapers: str = 'broadcast'

    def __post_init__(self):
        """Set user picks and fill rest with sensible defaults."""
        super().__post_init__()

    @property
    def multitaper_stft_args(self):
        """Get keyword arguments for a call to compute_multitaper_stft."""
        args = {}
        for key in ['time_bandwidth', 'num_tapers', 'freq_resolution',
                    'apply_tapers', 'fs', 'nperseg', 'nstep', 'nfft',
                    'detrend_func', 'side', 'scale', 'axis', 'mode', 'padded',
                    'fmin', 'fmax', 'output_axis']:
            args[key] = getattr(self, key)
        return args


# ------------------------------------------------------------------------
# Top-level computation functions
#
# These functions take input data, run the option handling and execute whatever
# computations are needed


@set_verbose
def sw_periodogram(x,
                   # General STFT kwargs
                   fs=1.0, window_type='hann', nperseg=None, noverlap=None, nfft=None,
                   detrend='constant', return_onesided=True, mode='psd', scaling='density',
                   axis=-1, fmin=None, fmax=None, return_config=False, verbose=None):
    """Compute Periodogram by averaging across windows in a STFT.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    window_type : str or tuple or array_like, optional
        Desired window to use. If `window` is a string or tuple, it is
        passed to `get_window` to generate the window values, which are
        DFT-even by default. See `get_window` for a list of windows and
        required parameters. If `window` is array_like it will be used
        directly as the window and its length must be nperseg. Defaults
        to a Hann window.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the power spectral density ('density')
        where `Pxx` has units of V**2/Hz and computing the power
        spectrum ('spectrum') where `Pxx` has units of V**2, if `x`
        is measured in V and `fs` is measured in Hz. Defaults to
        'density'
    axis : int, optional
        Axis along which the periodogram is computed; the default is
        over the last axis (i.e. ``axis=-1``).
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    return_config : bool
        Indicate whether parameter configuration object should be returned
        alongside result (Default value = False)

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.
    config : PeriodogramConfig, optional
        Configuration object containing all parameters used to compute
        spectrum, optionally returned based on value of `return_config`.

    """
    # Config object stores options in one place and sets sensible defaults for
    # unspecified options given the data in-hand
    config = PeriodogramConfig(x.shape[axis], input_complex=np.any(np.iscomplex(x)),
                               average=None, fs=fs, window_type=window_type, nperseg=nperseg,
                               noverlap=noverlap, nfft=nfft, detrend=detrend, mode=mode,
                               return_onesided=return_onesided, scaling=scaling, axis=axis,
                               fmin=fmin, fmax=fmax, output_axis='auto')

    f, t, p = compute_stft(x, **config.stft_args)
    logging.debug(p.shape)

    if return_config:
        return f, t, p, config
    else:
        return f, t, p


@set_verbose
def periodogram(x, average='mean',
                # General STFT kwargs
                fs=1.0, window_type='hann', nperseg=None, noverlap=None, nfft=None,
                detrend='constant', return_onesided=True, mode='psd', scaling='density',
                axis=-1, fmin=None, fmax=None, return_config=False, verbose=None):
    """Compute Periodogram by averaging across windows in a STFT.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    average : { 'mean', 'median' }, optional
        Method to use when averaging periodograms. Defaults to 'mean'.
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    window_type : str or tuple or array_like, optional
        Desired window to use. If `window` is a string or tuple, it is
        passed to `get_window` to generate the window values, which are
        DFT-even by default. See `get_window` for a list of windows and
        required parameters. If `window` is array_like it will be used
        directly as the window and its length must be nperseg. Defaults
        to a Hann window.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the power spectral density ('density')
        where `Pxx` has units of V**2/Hz and computing the power
        spectrum ('spectrum') where `Pxx` has units of V**2, if `x`
        is measured in V and `fs` is measured in Hz. Defaults to
        'density'
    axis : int, optional
        Axis along which the periodogram is computed; the default is
        over the last axis (i.e. ``axis=-1``).
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    return_config : bool
        Indicate whether parameter configuration object should be returned
        alongside result (Default value = False)

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.
    config : PeriodogramConfig, optional
        Configuration object containing all parameters used to compute
        spectrum, optionally returned based on value of `return_config`.

    """
    # Config object stores options in one place and sets sensible defaults for
    # unspecified options given the data in-hand
    logging.info('Setting config options')
    config = PeriodogramConfig(x.shape[axis], input_complex=np.any(np.iscomplex(x)),
                               average=average, fs=fs, window_type=window_type, nperseg=nperseg,
                               noverlap=noverlap, nfft=nfft, detrend=detrend, mode=mode,
                               return_onesided=return_onesided, scaling=scaling, axis=axis,
                               fmin=fmin, fmax=fmax, output_axis='time_first')

    logging.info('Starting computation')
    f, t, p = compute_stft(x, **config.stft_args)

    logging.info('Averaging across first dim of result using method {0}'.format(config.average))
    if config.average == 'mean':
        p = np.nanmean(p, axis=0)
    elif config.average == 'median':
        p = np.nanmedian(p, axis=0)
    elif config.average is None:
        pass
    else:
        msg = "'average' value of '{0}' not recognised - please use 'mean' or 'median'"
        raise ValueError(msg.format(config.average))

    logging.info('Returning spectrum of shape {0}'.format(p.shape))
    if return_config:
        return f, p, config
    else:
        return f, p


@set_verbose
def sw_multitaper(x, num_tapers='auto', freq_resolution=1, time_bandwidth=5, apply_tapers='broadcast',
                  # General STFT kwargs
                  fs=1.0, nperseg=None, noverlap=None, nfft=None,
                  detrend='constant', return_onesided=True, mode='psd', scaling='density',
                  axis=-1, fmin=None, fmax=None, return_config=False, verbose=None):
    """Compute a multi-tapered power spectrum across windows in a STFT.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    num_tapers : {int, 'auto'}
        The number of tapers to use if set to an integer value, if set to
        `'auto'` then the number of tapers is automatically computed from
        `freq_resolution` and `time_bandwidth` (Default value = 'auto')
    freq_resolution : int
        Required frequency resolution of the tapers used if `num_tapers` is set
        to `auto` (Default value = 1)
    time_bandwidth : int
        Required time bandwidth value of the tapers used if `num_tapers` is set
        to `auto` (Default value = 5)
    apply_tapers : {'broadcast', 'loop'}
        Flag indicating whether to estimate all tapers at once by broadcasting
        or one at a time in a loop.
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the power spectral density ('density')
        where `Pxx` has units of V**2/Hz and computing the power
        spectrum ('spectrum') where `Pxx` has units of V**2, if `x`
        is measured in V and `fs` is measured in Hz. Defaults to
        'density'
    axis : int, optional
        Axis along which the periodogram is computed; the default is
        over the last axis (i.e. ``axis=-1``).
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    return_config : bool
        Indicate whether parameter configuration object should be returned
        alongside result (Default value = False)

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.
    config : MultiTaperConfig, optional
        Configuration object containing all parameters used to compute
        spectrum, optionally returned based on value of `return_config`.

    """
    # Config object stores options in one place and sets sensible defaults for
    # unspecified options given the data in-hand
    config = MultiTaperConfig(x.shape[axis],
                              input_complex=np.any(np.iscomplex(x)),
                              time_bandwidth=time_bandwidth,
                              num_tapers=num_tapers, apply_tapers=apply_tapers,
                              freq_resolution=freq_resolution, average=None,
                              fs=fs, window_type=None, nperseg=nperseg,
                              noverlap=noverlap, nfft=nfft, detrend=detrend,
                              return_onesided=return_onesided, mode=mode,
                              scaling=scaling, axis=axis, fmin=fmin, fmax=fmax,
                              output_axis='auto')

    f, t, p = compute_multitaper_stft(x, **config.multitaper_stft_args)

    if return_config:
        return f, t, p, config
    else:
        return f, t, p


@set_verbose
def multitaper(x, average='mean', num_tapers='auto',
               freq_resolution=1, time_bandwidth=5, apply_tapers='broadcast',
               # General STFT kwargs
               fs=1.0, nperseg=None, noverlap=None, nfft=None,
               detrend='constant', return_onesided=True, scaling='density', mode='psd',
               axis=-1, fmin=None, fmax=None, return_config=False, verbose=None):
    """Compute a multi-tapered power spectrum averaged across windows in a STFT.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    average : { 'mean', 'median' }, optional
        Method to use when averaging periodograms. Defaults to 'mean'.
    num_tapers : {int, 'auto'}
        The number of tapers to use if set to an integer value, if set to
        `'auto'` then the number of tapers is automatically computed from
        `freq_resolution` and `time_bandwidth` (Default value = 'auto')
    freq_resolution : int
        Required frequency resolution of the tapers used if `num_tapers` is set
        to `auto` (Default value = 1)
    time_bandwidth : int
        Required time bandwidth value of the tapers used if `num_tapers` is set
        to `auto` (Default value = 5)
    apply_tapers : {'broadcast', 'loop'}
        Flag indicating whether to estimate all tapers at once by broadcasting
        or one at a time in a loop.
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the power spectral density ('density')
        where `Pxx` has units of V**2/Hz and computing the power
        spectrum ('spectrum') where `Pxx` has units of V**2, if `x`
        is measured in V and `fs` is measured in Hz. Defaults to
        'density'
    axis : int, optional
        Axis along which the periodogram is computed; the default is
        over the last axis (i.e. ``axis=-1``).
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    return_config : bool
        Indicate whether parameter configuration object should be returned
        alongside result (Default value = False)

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.
    config : MultiTaperConfig, optional
        Configuration object containing all parameters used to compute
        spectrum, optionally returned based on value of `return_config`.

    """
    # Config object stores options in one place and sets sensible defaults for
    # unspecified options given the data in-hand
    config = MultiTaperConfig(x.shape[axis],
                              input_complex=np.any(np.iscomplex(x)),
                              time_bandwidth=time_bandwidth,
                              num_tapers=num_tapers, apply_tapers=apply_tapers,
                              freq_resolution=freq_resolution, average=average,
                              fs=fs, window_type=None, nperseg=nperseg,
                              noverlap=noverlap, nfft=nfft, detrend=detrend,
                              return_onesided=return_onesided, mode=mode,
                              scaling=scaling, axis=axis, fmin=fmin, fmax=fmax,
                              output_axis='time_first')

    f, t, p = compute_multitaper_stft(x, **config.multitaper_stft_args)

    if config.average == 'mean':
        p = np.nanmean(p, axis=0)
    elif config.average == 'median':
        p = np.nanmedian(p, axis=0)
    else:
        msg = "'average' value of '{0}' not recognised - please use 'mean' or 'median'"
        raise ValueError(msg.format(config.average))

    if return_config:
        return f, p, config
    else:
        return f, p


# -----------------------------------------------------------------------
# GLM Spectrogram Functions


def _is_sklearn_estimator(fit_method):
    """Check (in the duck sense) if object is a skearn fitter.

    Parameters
    ----------
    fit_method : obj
        Initialised sklearn fitter object

    Returns
    -------
    bool
        flag indicating whether obj is a likely sklearn fitter

    """
    test1 = hasattr(fit_method, 'fit') and callable(getattr(fit_method, 'fit'))
    test2 = hasattr(fit_method, 'get_params') and callable(getattr(fit_method, 'get_params'))
    test3 = hasattr(fit_method, 'set_params') and callable(getattr(fit_method, 'set_params'))

    return test1 and test2 and test3


def _compute_ols_varcopes(design_matrix, data, contrasts, betas):
    """Compute variance of cope estimates.

    Parameters
    ----------
    design_matrix : ndarray
        Matrix specifying GLM design matrix of shape [num_observations x num_regressors]
    data : ndarray
        Matrix of data to be fitted
    contrasts : ndarray
        Matrix of contrasts
    betas : ndarray
        Array of fitted regression parameters

    Returns
    -------
    ndarray
        Standard error of GLM parameter estimates

    """
    # Compute varcopes
    varcopes = np.zeros((contrasts.shape[0], data.shape[1]))

    # Compute varcopes
    residue_forming_matrix = np.linalg.pinv(design_matrix.T.dot(design_matrix))
    var_forming_matrix = np.diag(np.linalg.multi_dot([contrasts,
                                                     residue_forming_matrix,
                                                     contrasts.T]))

    resid = data - design_matrix.dot(betas)

    # This is equivalent to >> np.diag( resid.T.dot(resid) )
    resid_dots = np.einsum('ij,ji->i', resid.T, resid)
    del resid
    dof_error = data.shape[0] - np.linalg.matrix_rank(design_matrix)
    V = resid_dots / dof_error
    varcopes = var_forming_matrix[:, None] * V[None, :]

    return varcopes


def _process_regressor(Y, config, mode='confound'):
    """Prepare a vector of data into a STFT regressor.

    Y is [nregs x nsamples]. Confound is scaled 0->1 and covariate is z-transformed.

    Parameters
    ----------
    Y : ndarray
        Covariate vector
    config : obj
        Initialised object of STFT options
    mode :  {'covariate', 'confound', 'None'}
        Type of regressor to create (Default value = 'confound')

    Returns
    -------
    ndarray
        Processed regressor

    """
    window = None if mode == 'condition' else config.window
    windowed = apply_sliding_window(Y, config.nperseg, config.nstep,
                                    window=window, padded=config.padded)

    y = np.nansum(windowed, axis=-1)
    print(config.nperseg)

    if mode == 'condition':
        y = y / config.nperseg
    elif mode == 'covariate':
        y = stats.zscore(y, axis=-1)
    elif mode == 'confound':
        y = y - y.min(axis=-1)[:, np.newaxis]
        y = y / y.max(axis=-1)[:, np.newaxis]
    elif mode is None:
        pass

    return y


def _process_input_covariate(cov, input_len):
    """Prepare and check user specified GLM covariates.

    Parameters
    ----------
    cov :{dict, None, ndarray}
        Specified covariates. One of a dictionary of vectors, a vector array, a
        [num_regressors x num_samples] array or None.
    input_len : int
        Number of samples in input data

    Returns
    -------
    dict
        Set of covariates

    """
    if isinstance(cov, dict):
        # We have a dictionary - ensure every entry is array_like numeric vector with
        # expected length
        for key, var in cov.items():
            if len(cov[key]) != input_len:
                msg = "Regressor '{0}' shape ({1}) not matched to input data length ({2})"
                raise ValueError(msg.format(key, len(cov[key]), input_len))
        ret = cov  # pass back out
    elif cov is None:
        ret = {}  # No regressors defined
    else:
        # Check array_like inputs
        cov = np.array(cov)
        if np.issubdtype(cov.dtype, np.number) is False:
            msg = "Regressor inputs must be numeric in type - input has type '{0}'"
            raise ValueError(msg.format(cov.dtype))

        # Add dummy dim if input is vector
        if cov.ndim == 1:
            cov = cov[np.newaxis, :]

        # Check length of regressors are correct
        if cov.shape[1] != input_len:
            msg = 'Regressor shape ({0}) not matched to input data length ({1})'
            raise ValueError(msg.format(cov.shape[1], input_len))

        # Give regressor a dummy name
        ret = {}
        for ii in range(cov.shape[0]):
            ret[chr(65 + ii)] = cov[ii, :]

    return ret


def _specify_design(conditions, covariates, confounds, config, fit_constant=True):
    """Create a design matrix.

    Parameters
    ----------
    covariates : dict
        Dictionary of covariate variables
    confounds : dict
        Dictionary of confound variables
    config : obj
        User specified STFT options
    fit_constant : bool
        Flag indicating whether to include a constant term (Default value = True)

    Returns
    -------
    design_matrix : ndarray
        [num_observations x num_regressors] matrix of regressors
    contrasts : ndarray
        [num_regressors x num_regressors] matrix of contrasts (identity)
    Xlabels : list of str
        List of regressor names

    """
    X = []
    Xlabels = []
    if fit_constant:
        logging.info("Adding constant")
        X.append(np.ones((config.nwindows,)))
        Xlabels.append('Constant')

    # Add conditions
    for idx, var in enumerate(conditions.keys()):
        logging.info("Adding condition '{0}'".format(var))
        X.append(_process_regressor(conditions[var], config, mode='condition'))
        Xlabels.append(var)
    # Add covariates
    for idx, var in enumerate(covariates.keys()):
        logging.info("Adding covariate '{0}'".format(var))
        X.append(_process_regressor(covariates[var], config, mode='covariate'))
        Xlabels.append(var)
    # Add confounds
    for idx, var in enumerate(confounds.keys()):
        logging.info("Adding confound '{0}'".format(var))
        X.append(_process_regressor(covariates[var], config, mode='confound'))
        Xlabels.append(var)

    design_matrix = np.vstack(X).T
    contrasts = np.eye(design_matrix.shape[1])

    return design_matrix, contrasts, Xlabels


def _run_prefit_checks(data, design_matrix, contrasts):
    """Run a few checks to catch likely errors in GLM fit.

    Parameters
    ----------
    data : ndarray
        Matrix of data to be fitted
    design_matrix : ndarray
        Matrix specifying GLM design matrix of shape [num_observations x num_regressors]
    contrasts : ndarray
        Matrix of contrasts

    Returns
    -------
    None


    """
    # Make sure we're set for model fitting
    assert(data.shape[0] == design_matrix.shape[0])
    assert(design_matrix.shape[1] == contrasts.shape[0])


def _glm_fit_simple(pxx, conditions, covariates, confounds, config, fit_method='pinv', fit_constant=True):
    """Fit a GLM using a standard OLS fitting method.

    Parameters
    ----------
    pxx : ndarray
        Power spectrum estimate with sliding windows in the first dimension
    covariates : dict
        Dictionary of covariate variables
    confounds : dict
        Dictionary of confound variables
    config : obj
        User specified STFT options
    fit_method : {'pinv', 'lstsq'}
        Fitting method to use (Default value = 'pinv')
    fit_constant : bool
        Flag indicating whether to fit a constant (Default value = True)

    Returns
    -------
    copes : ndarray
        array of fitted parameter estimates
    varcopes : ndarray
        array of standard errors of parameter estimates

    """
    # Prepare GLM components
    design_matrix, contrasts, Xlabels = _specify_design(conditions, covariates, confounds,
                                                        config, fit_constant=fit_constant)

    # Check we're probably good to go
    _run_prefit_checks(pxx, design_matrix, contrasts)

    # Compute parameters
    if fit_method == 'pinv':
        logging.debug('using np.linalg.pinv')
        betas = np.linalg.pinv(design_matrix).dot(pxx)
    elif fit_method == 'lstsq':
        logging.debug('using np.linalg.lstsq')
        betas, resids, rank, s = np.linalg.lstsq(design_matrix, pxx)
    else:
        raise ValueError("'fit_method' input {0} not recognised".format(fit_method))

    # Compute COPES and VARCOPES
    copes = contrasts.dot(betas)
    varcopes = _compute_ols_varcopes(design_matrix, pxx, contrasts, betas)

    return copes, varcopes


def _glm_fit_sklearn_estimator(pxx, conditions, covariates, confounds, config, fit_method, fit_constant=True):
    """Fit a GLM using a sklearn-like estimator object.

    Parameters
    ----------
    pxx : ndarray
        Power spectrum estimate with sliding windows in the first dimension
    covariates : dict
        Dictionary of covariate variables
    confounds : dict
        Dictionary of confound variables
    config : obj
        User specified STFT options
    fit_constant : bool
        Flag indicating whether to fit a constant (Default value = True)

    Returns
    -------
    copes : ndarray
        array of fitted parameter estimates
    varcopes : ndarray
        array of standard errors of parameter estimates
    fitter : obj
        sklearn fitting object

    """
    logging.info('Running sklearn GLM fit')
    # Prepare GLM components
    design_matrix, contrasts, Xlabels = _specify_design(conditions, covariates, confounds,
                                                        config, fit_constant=fit_constant)

    # Check we're probably good to go
    _run_prefit_checks(pxx, design_matrix, contrasts)

    # Compute parameters
    fit_method.fit(design_matrix, pxx)
    if hasattr(fit_method, 'coef_'):
        betas = fit_method.coef_.T
    else:
        # Sometimes this is stored in a sub model...
        betas = fit_method.estimator_.coef_.T

    # Compute COPES and VARCOPES
    copes = contrasts.dot(betas)
    varcopes = _compute_ols_varcopes(design_matrix, pxx, contrasts, betas)

    return copes, varcopes, (fit_method)


def _glm_fit_glmtools(pxx, conditions, covariates, confounds,
                      config, contrasts=None, fit_constant=True):
    """Fit a GLM using the glmtools package.

    Parameters
    ----------
    pxx : ndarray
        Power spectrum estimate with sliding windows in the first dimension
    covariates : dict
        Dictionary of covariate variables
    confounds : dict
        Dictionary of confound variables
    config : obj
        User specified STFT options
    fit_constant : bool
        Flag indicating whether to fit a constant (Default value = True)

    Returns
    -------
    copes : ndarray
        array of fitted parameter estimates
    varcopes : ndarray
        array of standard errors of parameter estimates
    extras : tuple
        Tuple containing glmtools model, design and data objects

    """
    logging.info('Running glmtools GLM fit')
    import glmtools as glm  # keep this as a soft dependency

    # Allocate GLM data object
    data = glm.data.TrialGLMData(data=pxx)

    # Add windowed confounds and covariates - no preproc yet
    for key, value in conditions.items():
        logging.debug('Processing Condition Regressor : {0}'.format(key))
        data.info[key] = _process_regressor(value, config, mode='condition')
    for key, value in covariates.items():
        data.info[key] = _process_regressor(value, config, mode=None)
    for key, value in confounds.items():
        data.info[key] = _process_regressor(value, config, mode=None)

    DC = glm.design.DesignConfig()
    if fit_constant:
        logging.debug('Adding Constant Regressor')
        DC.add_regressor(name='Constant', rtype='Constant')
    for key in conditions.keys():
        logging.debug('Adding Condition : {0}'.format(key))
        DC.add_regressor(name=key, rtype='Categorical', datainfo=key, codes=[1])
    for key in covariates.keys():
        logging.debug('Adding Covariate : {0}'.format(key))
        DC.add_regressor(name=key, rtype='Parametric', datainfo=key, preproc='z')
    for key in confounds.keys():
        logging.debug('Adding Confound : {0}'.format(key))
        DC.add_regressor(name=key, rtype='Parametric', datainfo=key, preproc='unitmax')

    if contrasts is not None:
        for con in contrasts:
            DC.add_contrast(**con)
    DC.add_simple_contrasts()

    des = DC.design_from_datainfo(data.info)

    model = glm.fit.OLSModel(des, data)

    return model.copes, model.varcopes, (model, des, data)


@set_verbose
def glm_periodogram(X, conditions=None, covariates=None, confounds=None,
                    contrasts=None, fit_method='pinv', fit_constant=True,
                    # General STFT kwargs
                    fs=1.0, window_type='hann', nperseg=None, noverlap=None, nfft=None,
                    detrend='constant', return_onesided=True, scaling='density',
                    axis=-1, mode='psd', fmin=None, fmax=None, verbose=None):
    """Compute a Power Spectrum with a General Linear Model.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    covariates : dict or None
        Dictionary of covariate time series to be added as z-standardised regessors. (Default value = None)
    confounds : dict or None
        Dictionary of confound time series to be added as positive-valued unitmax regessors. (Default value = None)
    fit_method : {'pinv', 'lstsq', 'glmtools', sklearn estimator instance}
        Specifies how the GLM parameters will be estimated.
        * `pinv` uses the design matrix psuedo-inverse method
        * `lstsq` uses np.linalg.lstsq.
        * `glmtools` uses the OLSModel from the glmtools package.
        * A parametrised instance of a sklearn estimator is used if specified here. (Default value = 'pinv')
    fit_constant : bool
        Specifies whether a constant valued 'intercept' regressor is included in the model. (Default value = True)
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the power spectral density ('density')
        where `Pxx` has units of V**2/Hz and computing the power
        spectrum ('spectrum') where `Pxx` has units of V**2, if `x`
        is measured in V and `fs` is measured in Hz. Defaults to
        'density'
    axis : int, optional
        Axis along which the periodogram is computed; the default is
        over the last axis (i.e. ``axis=-1``).
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    return_config : bool
        Indicate whether parameter configuration object should be returned
        alongside result (Default value = False)

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.
    extras : tuple
        Additional model information depending on the fit method used.

    """
    # Option housekeeping
    if axis == -1:
        axis = X.ndim - 1

    if X.ndim != 1 and fit_method in ['pinv', 'lstsq']:
        msg = "Data input should be vector for 'pinv' and 'lstsq' fits - data shape {0} was passed in"
        logging.error(msg.format(X.shape))
        logging.error("Use fit_method='glmtools' for multdimensional data")
        raise ValueError("Fit methods 'pinv' and 'lstsq' not implemented for multidimensional data")

    # Set configuration
    logging.info('Setting config options')
    config = GLMPeriodogramConfig(X.shape[axis], covariates=covariates,
                                  confounds=confounds, fit_method=fit_method,
                                  fit_constant=fit_constant, input_complex=np.iscomplexobj(X),
                                  fs=fs, fmin=fmin, fmax=fmax, window_type=window_type,
                                  nperseg=nperseg, noverlap=noverlap,
                                  nfft=nfft, detrend=detrend,
                                  return_onesided=return_onesided,
                                  scaling=scaling, axis=axis, mode=mode,
                                  output_axis='time_first')

    # Transform inputs into predicable, sanity checked dictionaries
    logging.info('Processing Conditions, Covariates and Confounds')
    conditions = _process_input_covariate(conditions, config.input_len)
    covariates = _process_input_covariate(covariates, config.input_len)
    confounds = _process_input_covariate(confounds, config.input_len)

    # Compute STFT
    logging.info('Computing sliding window periodogram')
    f, t, p = compute_stft(X, **config.stft_args)

    # Compute model - each method MUST assign copes, varcopes and extras
    if fit_method in ['pinv', 'lstsq']:
        logging.info('Running numpy GLM fit')
        copes, varcopes = _glm_fit_simple(p, conditions, covariates, confounds, config,
                                          fit_method=fit_method,
                                          fit_constant=fit_constant)
        extras = None
    elif fit_method == 'glmtools':
        logging.info('Running glmtools GLM fit')
        copes, varcopes, extras = _glm_fit_glmtools(p, conditions, covariates,
                                                    confounds, config,
                                                    contrasts=contrasts,
                                                    fit_constant=fit_constant)
    elif _is_sklearn_estimator(fit_method):
        logging.info('Running sklearn GLM fit with {0}'.format(_glm_fit_sklearn_estimator))
        copes, varcopes, extras = _glm_fit_sklearn_estimator(p, conditions, covariates, confounds, config,
                                                             fit_method=fit_method,
                                                             fit_constant=fit_constant)
    else:
        raise ValueError('fit_method not recognised')

    return f, copes, varcopes, extras


@set_verbose
def glm_multitaper(X, covariates=None, confounds=None, fit_method='pinv', fit_constant=True,
                   # Multitaper kwargs
                   num_tapers='auto', freq_resolution=1, time_bandwidth=5, apply_tapers='broadcast',
                   # General STFT kwargs
                   fs=1.0, window_type='hann', nperseg=None, noverlap=None, nfft=None,
                   detrend='constant', return_onesided=True, scaling='density',
                   axis=-1, mode='psd', fmin=None, fmax=None, verbose=None):
    """Compute a Power Spectrum with a General Linear Model.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    covariates : dict or None
        Dictionary of covariate time series to be added as z-standardised regessors. (Default value = None)
    confounds : dict or None
        Dictionary of confound time series to be added as positive-valued unitmax regessors. (Default value = None)
    fit_method : {'pinv', 'lstsq', 'glmtools', sklearn estimator instance}
        Specifies how the GLM parameters will be estimated.
        * `pinv` uses the design matrix psuedo-inverse method
        * `lstsq` uses np.linalg.lstsq.
        * `glmtools` uses the OLSModel from the glmtools package.
        * A parametrised instance of a sklearn estimator is used if specified here. (Default value = 'pinv')
    fit_constant : bool
        Specifies whether a constant valued 'intercept' regressor is included in the model. (Default value = True)
    num_tapers : {int, 'auto'}
        The number of tapers to use if set to an integer value, if set to
        `'auto'` then the number of tapers is automatically computed from
        `freq_resolution` and `time_bandwidth` (Default value = 'auto')
    freq_resolution : int
        Required frequency resolution of the tapers used if `num_tapers` is set
        to `auto` (Default value = 1)
    time_bandwidth : int
        Required time bandwidth value of the tapers used if `num_tapers` is set
        to `auto` (Default value = 5)
    apply_tapers : {'broadcast', 'loop'}
        Flag indicating whether to estimate all tapers at once by broadcasting
        or one at a time in a loop.
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    nperseg : int, optional
        Length of each segment. Defaults to None, but if window is str or
        tuple, is set to 256, and if window is array_like, is set to the
        length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to 'constant'.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    scaling : { 'density', 'spectrum' }, optional
        Selects between computing the power spectral density ('density')
        where `Pxx` has units of V**2/Hz and computing the power
        spectrum ('spectrum') where `Pxx` has units of V**2, if `x`
        is measured in V and `fs` is measured in Hz. Defaults to
        'density'
    axis : int, optional
        Axis along which the periodogram is computed; the default is
        over the last axis (i.e. ``axis=-1``).
    fmin : float or None, optional
        Minimum frequency value to return (Default value = 0)
    fmax : float or None, optional
        Maximum frequency value to return (Default value = 0.5)
    return_config : bool
        Indicate whether parameter configuration object should be returned
        alongside result (Default value = False)

    Returns
    -------
    freqs : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of times corresponding to each data segment
    result : ndarray
        Array of output data, contents dependent on *mode* kwarg.
    extras : tuple
        Additional model information depending on the fit method used.

    """
    # Option housekeeping
    if axis == -1:
        axis = X.ndim - 1

    if X.ndim != 1 and fit_method in ['pinv', 'lstsq']:
        msg = "Data input should be vector for 'pinv' and 'lstsq' fits - data shape {0} was passed in"
        logging.error(msg.format(X.shape))
        logging.error("Use fit_method='glmtools' for multdimensional data")
        raise ValueError("Fit methods 'pinv' and 'lstsq' not implemented for multidimensional data")

    # Set configuration
    logging.info('Setting config options')
    config = MultiTaperConfig(X.shape[axis],
                              input_complex=np.any(np.iscomplex(X)),
                              time_bandwidth=time_bandwidth,
                              num_tapers=num_tapers, apply_tapers=apply_tapers,
                              freq_resolution=freq_resolution, average=None,
                              fs=fs, window_type=None, nperseg=nperseg,
                              noverlap=noverlap, nfft=nfft, detrend=detrend,
                              return_onesided=return_onesided, mode=mode,
                              scaling=scaling, axis=axis, fmin=fmin, fmax=fmax,
                              output_axis='auto')

    logging.info('Processing Covariates and Confounds')
    covariates = _process_input_covariate(covariates, config.input_len)
    confounds = _process_input_covariate(confounds, config.input_len)

    # Compute STMT
    logging.info('Computing sliding window multitaper')
    f, t, p = compute_multitaper_stft(X, **config.multitaper_stft_args)

    # Compute model - each method MUST assign copes, varcopes and extras
    if fit_method in ['pinv', 'lstsq']:
        logging.info('Running numpy GLM fit')
        copes, varcopes = _glm_fit_simple(p, covariates, confounds, config,
                                          fit_method=fit_method,
                                          fit_constant=fit_constant)
        extras = None
    elif fit_method == 'glmtools':
        logging.info('Running glmtools GLM fit')
        copes, varcopes, extras = _glm_fit_glmtools(p, covariates, confounds, config,
                                                    fit_constant=fit_constant)
    elif _is_sklearn_estimator(fit_method):
        logging.info('Running sklearn GLM fit with {0}'.format(_glm_fit_sklearn_estimator))
        copes, varcopes, extras = _glm_fit_sklearn_estimator(p, covariates, confounds, config,
                                                             fit_method=fit_method,
                                                             fit_constant=fit_constant)
    else:
        raise ValueError('fit_method not recognised')

    return f, copes, varcopes, extras
