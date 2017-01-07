import numpy, scipy.io.wavfile,matplotlib.pyplot as plt
from mysignal import play, tone

def mag2dB(x):
    return 20 * numpy.log10(x / max(x))

def plotfft(x, sampling_rate=1,logscale=False):
    f=numpy.fft.rfft(x)
    mag=numpy.abs(f)
    #mag[mag<0.1]=0

    fig1 = plt.figure()
    if logscale:
        mag=mag2dB(mag)
    plt.plot(numpy.arange(mag.size,dtype=numpy.float32)/mag.size*sampling_rate/2, mag, color="g")
    #deltafreq=rate/mag.size
    plt.show()

def find_tones(x, sampling_rate=1, tresh=0.8, logscale=False):
    f=numpy.fft.rfft(x)
    #f=f[:f.size/2]
    mag=numpy.abs(f)
    if logscale:
        mag=mag2dB(mag)
    return numpy.where(mag>tresh*numpy.max(mag))[0]*sampling_rate/(mag.size*2)

def signalogram(x,frame_size=512, overlap=0.5):
    advance=int(frame_size*overlap)
    size = int(numpy.ceil(x.size / advance))
    ret=numpy.zeros(shape=(frame_size, size))
    for i in range(size):
        frame = x[int(advance * i):int(advance * i + frame_size)]
        frame=numpy.hstack((frame,numpy.zeros(frame_size-frame.size)))
        ret[:,i]= frame
    return ret

def plotSignalogram(signal,frame_size=512):
    sgnmat = signalogram(signal, frame_size)
    ft=numpy.abs(numpy.fft.rfft(sgnmat, axis=0))#*numpy.hamming(frame_size)
    print(sgnmat.shape,ft.shape)
    fig1 = plt.figure()
    plt.imshow(ft, cmap="hot", origin="lower")
    plt.show()

if __name__=="__main__":
    rate, signal = scipy.io.wavfile.read("zvizg.wav")
    plotSignalogram(signal)
    """def f(x):
        return numpy.convolve(x,(0.2,0.2,0.2,0.2,0.2))
    ins=f(tone(250, 1000, 1, 3, 0))
    fftlength=512
    plotfft(numpy.hstack(((0.2,0.2,0.2,0.2,0.2), numpy.zeros(fftlength-5))),1000)
"""
    """
    signal = tone(24, 50, 3, 0.45, 0) + tone(6.01, 50, 3, 0.9, 0)
    #rate,signal=scipy.io.wavfile.read("aaa.wav")
    print(find_tones(signal,50,0.5))
    plotfft(signal,50)"""