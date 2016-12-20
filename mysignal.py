import numpy,scipy.io.wavfile,scipy.signal,os,matplotlib.pyplot as plt


SAMPLE_RATE = 44100
TIME = 3 #v s

def play(tab,rate=SAMPLE_RATE):
    #PLAYER="c:\\dps\\scilab\\bin\\mplay32"
    TMP_FN = "tmp.wav"
    scipy.io.wavfile.write(TMP_FN, rate, numpy.array(tab/numpy.max(numpy.abs(tab))*(2**30),dtype=numpy.int32))
    #os.popen(PLAYER+" "+TMP_FN)
    os.popen(TMP_FN)

def tone(freq,sample_rate=SAMPLE_RATE,time=TIME,volume=0.7, phase_angle=0):
    return volume * numpy.sin(numpy.arange(float(sample_rate * time)) / sample_rate * 2 * numpy.pi * freq + phase_angle)

def avg(s):
    return numpy.convolve(s,[0.1]*10)

C=0.8
def iir1(s):
    b=[1-C]
    a=[1,-C]
    return scipy.signal.lfilter(b,a,s)

def iir2(s):
    b=[1-C]
    a=[1,C]
    return scipy.signal.lfilter(b,a,s)

def FM(freq,freqMod,amMod,recursion=1,sample_rate=SAMPLE_RATE,time=TIME,volume=0.7):
    samples=numpy.arange(sample_rate * time)*2*numpy.pi/sample_rate
    res=numpy.sin(freqMod*samples)
    for i in range(recursion):
        res=numpy.sin(freqMod*samples + amMod*res)
    return volume*numpy.sin(freq*samples + amMod*res)

def iir3(s):
    b=[1-C]
    a=[2,C]
    return scipy.signal.lfilter(b,a,s)

def odmev(s,sample_rate=SAMPLE_RATE):
    a=numpy.zeros(sample_rate)
    a[0]=1
    a[-1]=0.5
    return numpy.convolve(s, a)

if __name__=="__main__":

    FREQ = 200

    # inS = tone(200) + tone(3800, volume=0.3)
    # s1 = iir1(inS)
    # s2 = iir2(inS)
    # play(numpy.hstack([inS, s1, s2]))
    #
    # PLOT_SAMPLES = 150
    # fig1=plt.figure()
    # plt.plot(inS[:PLOT_SAMPLES], color="r")
    # plt.plot(s1[:PLOT_SAMPLES], color="g")
    # plt.plot(s2[:PLOT_SAMPLES], color="b")
    # plt.show()
    """
    inS = tone(200) + tone(3800, volume=0.3)
    s1 = iir1(inS)
    s2 = iir2(inS)
    play(numpy.hstack([inS, s1, s2]))

    PLOT_SAMPLES = 150
    fig1=plt.figure()
    plt.plot(inS[:PLOT_SAMPLES], color="r")
    plt.plot(s1[:PLOT_SAMPLES], color="g")
    plt.plot(s2[:PLOT_SAMPLES], color="b")
    plt.show()
    """
    play(numpy.hstack([tone(FREQ, time=2),
                       FM(FREQ, 2*FREQ, 0.5, 0),
                       FM(FREQ, 2*FREQ, 0.5, 1),
                       FM(FREQ, 2*FREQ, 0.5, 2),
                       FM(FREQ, 2*FREQ, 0.5, 4),
                       FM(FREQ, 2*FREQ, 0.5, 800)]))


    """rate,data=scipy.io.wavfile.read("runaway_mono.wav")
    play(odmev(data),rate)"""
    #play(tone(FREQ))