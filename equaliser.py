import numpy, scipy.signal
from freqencyAnalysis import plotfft
from mysignal import tone
from iir import plot_filter_response

freqs=[20,200,500,2000,5000,20000]
sampling_freq=44100
pbw=30
length=101

tmp = pbw / 2.
filters=[]
coeffs=scipy.signal.remez(length, [0,  freqs[1] - tmp, freqs[1] + tmp, 0.5 * sampling_freq - tmp], [1, 0], [1, 1], sampling_freq)
filter = lambda x,coeffs=coeffs: numpy.convolve(x, coeffs)
filters.append(filter)
for a,b in zip(freqs[1:-1],freqs[2:]):
    print a,b,tmp,[0, a - tmp, a + tmp, b - tmp, b + tmp, 0.5 * sampling_freq - tmp]
    coeffs=scipy.signal.remez(length, [0, a - tmp, a + tmp, b - tmp, b + tmp, 0.5 * sampling_freq - tmp], [0, 1, 0], [1, 1, 1], sampling_freq)
    filter = lambda x,coeffs=coeffs: numpy.convolve(x, coeffs)
    filters.append(filter)

for f in filters:
    plot_filter_response(f,sampling_freq,1024)
