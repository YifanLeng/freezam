import numpy
from scipy import signal
from scipy.signal import find_peaks
import scipy
import functools 
import matplotlib.pyplot as plt
############################################
#    Title: github source code
#    Author: nils-werner
#    Date: 2016
#    Code version: 1.0
#    Availability: https://gist.github.com/nils-werner/9d321441006b112a4b116a8387c2280c
def sliding_window(data, size, stepsize=1, padded=False, axis=-1, copy=True):
    """
    Calculate a sliding window over a signal
    Parameters
    ----------
    data : numpy array
        The array to be slided over.
    size : int
        The sliding window size
    stepsize : int
        The sliding window stepsize. Defaults to 1.
    axis : int
        The axis to slide over. Defaults to the last axis.
    copy : bool
        Return strided array as copy to avoid sideffects when manipulating the
        output array.
    Returns
    -------
    data : numpy array
        A matrix where row in last dimension consists of one instance
        of the sliding window.
    Notes
    -----
    - Be wary of setting `copy` to `False` as undesired sideffects with the
      output values may occurr.
    Examples
    --------
    >>> a = numpy.array([1, 2, 3, 4, 5])
    >>> sliding_window(a, size=3)
    array([[1, 2, 3],
           [2, 3, 4],
           [3, 4, 5]])
    >>> sliding_window(a, size=3, stepsize=2)
    array([[1, 2, 3],
           [3, 4, 5]])
    See Also
    --------
    pieces : Calculate number of pieces available by sliding
    """
    if axis >= data.ndim:
        raise ValueError(
            "Axis value out of range"
        )

    if stepsize < 1:
        raise ValueError(
            "Stepsize may not be zero or negative"
        )
 
    if size > data.shape[axis]:
        raise ValueError(
            "Sliding window size may not exceed size of selected axis"
        )

    shape = list(data.shape)
    shape[axis] = numpy.floor(data.shape[axis] / stepsize - size / stepsize + 1).astype(int)
    shape.append(size)

    strides = list(data.strides)
    strides[axis] *= stepsize
    strides.append(data.strides[axis])

    strided = numpy.lib.stride_tricks.as_strided(
        data, shape=shape, strides=strides
    )

    if copy:
        return strided.copy()
    else:
        return strided

def apply_windows(slided_signals, window_type="hann"):
    """
    apply the window function over the signals
    the length of the window is the same as the 
    length of the signal
    ----------
    slided_signals : numpy array
        The arrays to be windowed over.
    window_type: string, float, or tuple
        The type of window to create.
    Returns
    -------
    data : numpy array
        The same dimension as the input. 
    """
    # length of each slided signal
    n = slided_signals.shape[-1]
    window = signal.get_window(window_type, n)
    windowed_signals = numpy.multiply(slided_signals, window)
    return windowed_signals

def get_windowed_signals(signal, rate, window_type, width, shift):
    """
    slide the signal by width and shift and apply
    the window function on the slided signals
    ----------
    signals : numpy array
        The original time-series arrays to be  slided 
        and windowed over.
    rate : the sampling rate of the signal
    window_type : string, float, or tuple
        The type of window to create.
    width : int
        the width of the window in seconds
    shift : int
        the shift between two windows in seconds
    Returns
    -------
    data : numpy array
           its dimension is the number of windows x window length
    """
    size = width
    stepsize = shift
    signals = sliding_window(signal, size, stepsize)
    win_signals = apply_windows(signals, window_type)
    return win_signals

    
def get_spectrogram(rate, signal, width, shift, filename, plot, window_type="hann"):
    """
    slide the signal by width and shift and apply
    the window function on the slided signals
    for each windowed signal, compute and store its periodogram
    ----------
    signals : numpy array
        The original time-series arrays to be  slided 
        and windowed over.
    rate : the sampling rate of the signal
    window_type : string, float, or tuple
        The type of window to create.
    width : int
        the width of the window in seconds
    shift : int
        the shift between two windows in seconds
    Returns
    -------
    data : list
        an list of tuples (f_i, Pxx_i). The array length is the number of windows
        f_i is the array of sample frequencies at window i
        Pxx_i is the power spectral density of window i
    """
    win_signals = get_windowed_signals(signal, rate, window_type, width, shift)
    spectrogram = []
    for win_signal in win_signals:
        (f, Pxx) = scipy.signal.periodogram(win_signal, fs=rate, scaling='spectrum')
        spectrogram.append((f, Pxx))
    if plot:
        plot_name = "./spectrograms/"+filename[:-4]+".png"
        plt.specgram(signal,Fs=rate)
        plt.savefig(plot_name)
        plt.close()
    return spectrogram

def scale(x):
    """
    normalize x to a scale of 0 to 1
    convert x to list
    """
    min_x, max_x = numpy.min(x), numpy.max(x)
    if min_x != max_x:
        x  = (x-min_x)/(max_x-min_x)
    else:
        # all the numbers are the same in x
        x = numpy.asarray([1/len(x) for i in range(len(x)) ])
    return x.tolist()

def get_signature(spectrogram, k):
    """
    calculate the signature from the spectrogram, 
    which contain the local periodogram of each window
    ----------
    spectrogram : list
       a list of local periodogram (f,p) of each window
    k: int
       k peaks in a window's periodogram
    Returns
    -------
    data : list
        signature of each window - k positive frequencies that match the largest
        k peaks
    """
    signature = []
    for (f, p) in spectrogram:
        f_p = zip(f, p)
        # filter out the  0<frequencies < 5k
        f_p = list(filter(lambda x : 0 < x[0] < 5000, f_p))
        (f, p) = zip(*f_p)
        peak_indexes = find_peaks(p)[0]
        f_p_peaks = [(f[i], p[i]) for i in peak_indexes]
        # sort by power
        sort_by_power = sorted(f_p_peaks, key=lambda x: x[1], reverse=True)
        # retrive the frequencies with the k largest peaks in power
        k_largest_freq = numpy.asarray([fp[0] for fp in sort_by_power[0:k]])
        # scale the frequencies in the range of 0 to 1
        signature.append(scale(k_largest_freq))
    return signature
                

def get_constellation_map(spectrogram, filename, plot):
    window_id = 0
    constellation_map = []
    for (f, p) in spectrogram:
        peak_inds = find_peaks(p)[0]
        inds_powers = [(i, p[i]) for i in peak_inds]
        sort_by_power = sorted(inds_powers, key=lambda x: x[1], reverse=True)    
        # retrive the frequency indices with the k most intensity peaks in power
        k = 30
        points = [(window_id,ip[0]) for ip in sort_by_power[0:k]]
        window_id += 1
        constellation_map.append(points)
        # constellation_map.append(freq_inds)
    if plot:
        flat_const_map = functools.reduce(lambda x,y: x+y, constellation_map)
        plot_name = "./spectrograms/"+filename[:-4]+"_const_map.png"
        (window_id, freq_bins) = zip(*flat_const_map)
        plt.scatter(window_id, freq_bins, s=0.5)
        plt.savefig(plot_name)
        plt.close()
    return constellation_map

def combinatorial_hashing(constellation_map):
    # convert points to pairs
    n = len(constellation_map)
    del_t, del_f, fan_out = 35, 30, 10
    hash_value = []
    for i in range(n):
        for j in range(len(constellation_map[i])):
            pairs = 0 # track the number of pairs found
            t1, f1 = i, constellation_map[i][j][1]
            # pair with points vertically in the current window
            for k in range(j+1, len(constellation_map[i])):
                t2, f2 = i, constellation_map[i][k][1]
                if abs(f2-f1) < del_f:
                    if pairs < fan_out:
                        pairs += 1
                        hash_value.append((f1, f2, (t2-t1), t1))
                    else:
                        break
            # pair with points after the current window
            for w_k in range(i+1, min(i+1+del_t, n)):
                if pairs >= fan_out:
                    break
                for f_k in range(len(constellation_map[w_k])):
                    t2, f2 = w_k, constellation_map[w_k][f_k][1]
                    if abs(f2-f1) < del_f:
                        if pairs < fan_out:
                            pairs += 1
                            hash_value.append((f1, f2, (t2-t1), t1))
                        else:
                            break
    return hash_value
                




