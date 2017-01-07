import numpy, scipy.io.wavfile,matplotlib.pyplot as plt, scipy.signal
from mysignal import play, tone
from freqencyAnalysis import plotfft

def make_filter(zeros, poles):
    a=numpy.polynomial.polynomial.polyfromroots(zeros)
    a=numpy.real(a)
    if poles:
        b=numpy.polynomial.polynomial.polyfromroots(poles)
        b=numpy.real(b)
        return lambda x: scipy.signal.lfilter(a[::-1],b[::-1],x)
    else:
        return lambda x: numpy.convolve(x,a)

def make_notch(freq, sampling_freq):
    direction=numpy.e**(1j*numpy.pi*freq/sampling_freq*2)
    return make_filter([direction, numpy.conj(direction)],[0.937*direction, 0.937*numpy.conj(direction)])

def make_peak(freq, sampling_freq):
    direction=numpy.e**(1j*numpy.pi*freq/sampling_freq*2)
    return make_filter([],[0.937*direction, 0.937*numpy.conj(direction)])

def plot_filter_response(filter, sampling_frequency, resolution, logscale=True):
    impulse_response=filter([1]+[0]*(resolution-1))
    plotfft(impulse_response,sampling_frequency,logscale)


if __name__=="__main__":
    fs = 500
    #iir=make_filter([-1,1],[0.937j,-0.937j])
    iir=make_peak(50, fs)
    plot_filter_response(iir, fs, 1024,False)