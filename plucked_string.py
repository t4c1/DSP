import numpy, scipy.io
from mysignal import play, tone

def plucked_string(freq, time, pre_iters=0, filter=lambda x: 0.995 * (x * 0.6 + numpy.roll(x, 1) * 0.4),rate=44100, d=0.5):
    buf_len=round(rate/freq-d)
    iters=int(TIME * RATE / buf_len)

    #buffer=numpy.random.random(buf_len)*2

    #buffer=numpy.zeros(buf_len)
    #buffer[0]=buf_len/2

    #buffer=tone(freq*2**0.5,rate,buf_len/rate)
    buffer=tone(freq*2.1,rate,buf_len/rate)

    buffer-=numpy.mean(buffer)
    out=buffer[:]
    for i in range(pre_iters-1):
        buffer=filter(buffer)
    for i in range(iters-1):
        buffer=filter(buffer)
        out=numpy.hstack((out,buffer))
    return out

if __name__=="__main__":
    RATE=44100
    FREQ=200
    TIME=5 #s

    play(0.4 * numpy.hstack((plucked_string(FREQ, TIME, 0, lambda x: 0.97 * (x * 0.5 + numpy.roll(x, 1) * 0.5)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.98 * (x * 0.5 + numpy.roll(x, 1) * 0.5)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.99 * (x * 0.5 + numpy.roll(x, 1) * 0.5)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.5 + numpy.roll(x, 1) * 0.5)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.999 * (x * 0.5 + numpy.roll(x, 1) * 0.5)),

                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.6 + numpy.roll(x, 1) * 0.4)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.7 + numpy.roll(x, 1) * 0.3)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.8 + numpy.roll(x, 1) * 0.2)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.9 + numpy.roll(x, 1) * 0.1)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.95 + numpy.roll(x, 1) * 0.05)),
                             plucked_string(FREQ, TIME, 0, lambda x: 0.995 * (x * 0.98 + numpy.roll(x, 1) * 0.02)),
                             plucked_string(FREQ, TIME, 0, lambda x: 1.0 * (x * 0.5 + numpy.roll(x, 1) * 0.5)),
    )), RATE)