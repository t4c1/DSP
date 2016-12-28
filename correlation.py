import numpy, scipy.io.wavfile,matplotlib.pyplot as plt, scipy.signal
from mysignal import play, tone

def normalize(a):
    a-=numpy.average(a)
    return a/numpy.max(numpy.abs(a))

def freq_detect(inS,inS2=None, plot_samples=1000, rate=1, full=False):
    if inS2 is None:
        inS2=inS
    inS,inS2=normalize(inS.astype(numpy.float32)),normalize(inS2.astype(numpy.float32))
    corr=numpy.correlate(inS,inS2,"full")
    if full:
        to_plot=corr
    else:
        corr=corr[corr.shape[0]/2:]
        to_plot = corr[:plot_samples]
    #corr=corr[inS2.shape[0]-1:]
    x_os = (numpy.arange(to_plot.size)-(corr.shape[0]/2*full)) / float(rate)
    plt.plot(x_os, to_plot, color="g")
    plt.show()

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

def echo_amp_find(inS,delay):
    mina=-1
    mine=float("inf")
    for a in range(0,10):
        a/=10.0
        cleaned=numpy.convolve([1]+[0]*(delay-2)+[-a], inS)
        e=numpy.sum(cleaned*cleaned)
        if e<mine:
            mina=a
            mine=e
    mina2=-1
    mine2=float("inf")
    for a in range(-5,6):
        a2=mina+a/100.0
        cleaned=numpy.convolve([1]+[0]*(delay-2)+[-a2], inS)
        e=numpy.sum(cleaned*cleaned)
        if e<mine2:
            mina2=a2
            mine2=e
    return mina2

def find_rel_amp(in1,in2, one_sided=True):
    mina=0
    if not one_sided:
        mine=float("inf")
        for a in range(0,100):
            cleaned=in1-a/10.*in2
            e=numpy.sum(cleaned*cleaned)
            if e<mine:
                mina=a
                mine=e
    mina2=-1
    mine2=float("inf")
    for a in range(-5,6):
        a2=mina+a/10.0
        cleaned=in1-a2*in2
        e=numpy.sum(cleaned*cleaned)
        if e<mine2:
            mina2=a2
            mine2=e
    mina3=-1
    mine3=float("inf")
    for a in range(-5,6):
        a3=mina2+a/100.0
        cleaned=in1-a3*in2
        e=numpy.sum(cleaned*cleaned)
        if e<mine3:
            mina3=a3
            mine3=e
    return mina3

def find_rel_amp2(in1, in2, step=1.2, steps=20, iters=2):
    prevbest=1
    for i in range(iters):
        mina=0
        mine=float("inf")
        for a in prevbest*step**((numpy.arange(0,steps)-steps/2)/float((steps/2)**i)):
            cleaned=in1-a*in2
            e=numpy.sum(cleaned*cleaned)
            print a,"\t",e
            if e<mine:
                mina=a
                mine=e
        prevbest=mina
        print "picked",mina
    return prevbest

def echo_elimination():
    sampleRate,inS = scipy.io.wavfile.read("primer_odmev.wav")
    #_,inS2 = scipy.io.wavfile.read("primer.wav")
    freq_detect(inS,inS,100000,1)#rocno delo - iskanje odmeva iz grafa korelacije
    delay=4500
    mina=echo_amp_find(inS,delay)
    mina=find_rel_amp2(inS,numpy.roll(inS,delay))
    print "amplituda odmeva:",mina
    play(numpy.hstack((inS,numpy.convolve([1]+[0]*(delay-2)+[-mina], inS))),sampleRate)#primerjava originala in brez odmevov

def beamform_1():
    # sampleRate,inS = scipy.io.wavfile.read("mic_1a.wav")
    # fns = "mic_2a.wav", "mic_3a.wav", "mic_4a.wav", "mic_5a.wav"
    # shifts=[35,70,105,140] #prebrano iz grafov, narejenih z spodnjim zakomentiranim programom. Za drugega govorca mnozi z -1
    # shifted=[]
    # cleaned=[]
    # for fn,shift in zip(fns,shifts):
    #     shift*=-1
    #     _,inS2 = scipy.io.wavfile.read(fn)
    #     mina=1.0#find_rel_amp2(inS,numpy.roll(inS2,shift)) # ni potrebno - vsi signali imajo enako amplitudo
    #     shifted.append(numpy.roll(inS2,shift)*mina)
    #     cleaned.append(numpy.roll(inS2,shift)*mina-inS)
    # #play(sum(shifted)+inS,sampleRate)
    # play(sum(cleaned),sampleRate) #najboljsi rezultat
    # #play(inS-shifted[0]+shifted[1]-shifted[2],sampleRate)

    sampleRate,inS = scipy.io.wavfile.read("mic_1a.wav")
    sampleRate,in_ = scipy.io.wavfile.read("woman1.wav")
    _,inS2 = scipy.io.wavfile.read("mic_2a.wav")
    _,inS3 = scipy.io.wavfile.read("mic_3a.wav")
    _,inS4 = scipy.io.wavfile.read("mic_4a.wav")
    _,inS5 = scipy.io.wavfile.read("mic_5a.wav")
    freq_detect(inS,in_,10000,1,True)
    freq_detect(inS2,in_,10000,1,True)
    freq_detect(inS3,in_,10000,1,True)
    freq_detect(inS4,in_,10000,1,True)
    freq_detect(inS5,in_,10000,1,True)

def beamform_2():
    sampleRate,inS = scipy.io.wavfile.read("man1.wav")
    fns = "mic_1b.wav", "mic_2b.wav", "mic_3b.wav", "mic_4b.wav", "mic_5b.wav"
    #shifts=[-21,-39,-61,-78] #prebrano iz grafov, narejenih z spodnjim zakomentiranim programom.
    shifts=[0,20,40,60,80] #prebrano iz grafov, narejenih z spodnjim zakomentiranim programom.
    shifted=[]
    cleaned=[]
    for fn,shift in zip(fns,shifts):
        shift*=-1
        _,inS2 = scipy.io.wavfile.read(fn)
        mina=1.0#find_rel_amp2(inS,numpy.roll(inS2,shift)) # ni potrebno - vsi signali imajo enako amplitudo
        shifted.append(numpy.roll(inS2,shift)*mina)
        cleaned.append(numpy.roll(inS2,shift)*mina-inS)
    play(sum(shifted),sampleRate)
    #play(sum(cleaned),sampleRate) #najboljsi rezultat
    #play(inS-shifted[0]+shifted[1]-shifted[2],sampleRate)

    # sampleRate,inS = scipy.io.wavfile.read("man1.wav")
    # _,inS1 = scipy.io.wavfile.read("mic_1b.wav")
    # _,inS2 = scipy.io.wavfile.read("mic_2b.wav")
    # _,inS3 = scipy.io.wavfile.read("mic_3b.wav")
    # _,inS4 = scipy.io.wavfile.read("mic_4b.wav")
    # _,inS5 = scipy.io.wavfile.read("mic_5b.wav")
    # freq_detect(inS,inS5,10000,1,True)

if __name__ == "__main__":
    #echo_elimination()
    #beamform_1()

    for fn in "eight_mono1.wav","eight_mono2.wav","eight_mono3.wav","eight_mono4.wav","eight_mono5.wav":
            sampleRate,inS = scipy.io.wavfile.read(fn)
            freq_detect(inS[:,0],inS[:,1],10000,1,True)

    # rad=scipy.io.loadmat("radar.mat")
    # radar(numpy.ndarray.flatten(rad["paket"]),numpy.ndarray.flatten(rad["sent1"]),numpy.ndarray.flatten(rad["rec1"]))