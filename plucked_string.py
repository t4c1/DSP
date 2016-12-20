import numpy, scipy.io
from mysignal import play, tone

def plucked_string(buf_len, iters, pre_iters=0, filter=lambda x: 0.995 * (x * 0.6 + numpy.roll(x, 1) * 0.4)):
    #buffer=numpy.sin(numpy.arange(buf_len)*2 * numpy.pi)
    buffer=numpy.random.random(buf_len)*2-1
    print(buffer)
    out=buffer[:]
    for i in range(pre_iters-1):
        buffer=filter(buffer)
    for i in range(iters-1):
        buffer=filter(buffer)
        out=numpy.hstack((out,buffer))
    return out

def load_filters():
    a=scipy.io.loadmat("filtri.mat")
    return a["h1"],a["h2"],a["h3"],a["h4"],a["h5"]

if __name__=="__main__":
    RATE=44100
    FREQ=200
    TIME=2 #s

    buf_len = RATE / FREQ
    play(0.4 * plucked_string(buf_len, int(TIME * RATE / buf_len), 0), RATE)