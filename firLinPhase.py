import numpy, scipy.io.wavfile,matplotlib.pyplot as plt, scipy.signal
from mysignal import play, tone
from freqencyAnalysis import plotfft
from iir import plot_filter_response

def make_low_pass(freq, sampling_freq=1, length=129, window=None):
    """
    length:  mora bit liho stevilo
    """
    omega=2*numpy.pi*freq
    filter=numpy.zeros(length)
    filter[length//2]= (omega / sampling_freq) / numpy.pi
    for i in range(length//2):
        n=i-length//2
        filter[i]= numpy.sin(n * (omega / sampling_freq)) / (n * numpy.pi)
        filter[length-i-1]=filter[i]
    if window is not None:
        filter*=window
    return lambda x: numpy.convolve(x,filter)

def low_pass_remez(freq, sampling_freq=1.0, length=129, pbw=0.05):
    tmp = pbw / 2. /sampling_freq
    coeffs=scipy.signal.remez(length, [0, freq - tmp, freq + tmp, 0.5 * sampling_freq - tmp], [1, 0], [1, 1], sampling_freq)
    return lambda x: numpy.convolve(x, coeffs)

if __name__=="__main__":
    length=129
    #lp=make_low_pass(0.2,length=length, window=scipy.signal.chebwin(length,100))#numpy.kaiser(length,5.44)
    lp=low_pass_remez(0.2,length=length)
    plot_filter_response(lp,1,1024)