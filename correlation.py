import numpy, scipy.io.wavfile,matplotlib.pyplot as plt
from mysignal import play, tone

def freq_detect(inS):
    corr=numpy.correlate(inS,inS,"full")
    corr=corr[corr.shape[0]/2:]
    PLOT_SAMPLES = 150
    fig1 = plt.figure()
    #plt.plot(inS[:PLOT_SAMPLES], color="r")
    plt.plot(corr[:PLOT_SAMPLES], color="g")
    plt.show()

def normalize(a):
    a-=numpy.average(a)
    return a/numpy.max(numpy.abs(a))

def radar(paket,sent,recieved):
    #paket=normalize(paket)
    sent=normalize(sent)
    recieved=normalize(recieved)

    sent_corr = numpy.correlate(sent, paket, "full")
    sent_delay=numpy.argmax(sent_corr)-sent_corr.shape[0]/2
    rec_corr = numpy.correlate(recieved, paket, "full")
    rec_delay=numpy.argmax(rec_corr)-rec_corr.shape[0]/2
    correlate = numpy.correlate(recieved, sent, "full")
    cor_delay=numpy.argmax(correlate)-correlate.shape[0]/2
    print (sent_delay,rec_delay,cor_delay)
    fig1 = plt.figure()
    #plt.plot(sent_corr, color="g")
    plt.plot(numpy.arange(sent_corr.shape[0])-sent_corr.shape[0]/2, sent_corr, color="g")
    plt.plot(numpy.arange(rec_corr.shape[0])-rec_corr.shape[0]/2, rec_corr, color="r")
    #plt.plot(numpy.arange(correlate.shape[0])-correlate.shape[0]/2, correlate, color="b")
    plt.show()

if __name__ == "__main__":
    #sampleRate,inS = scipy.io.wavfile.read("aaa.wav")#tone(100,4000,0.1)
    #freq_detect(inS)

    rad=scipy.io.loadmat("radar.mat")
    radar(numpy.ndarray.flatten(rad["paket"]),numpy.ndarray.flatten(rad["sent1"]),numpy.ndarray.flatten(rad["rec1"]))