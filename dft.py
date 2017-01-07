import numpy
from freqencyAnalysis import plotfft
from mysignal import tone

rate=8000
#t=tone(1000,rate,32./rate)+tone(1100,rate,32./rate)
t=tone(1000,rate,64./rate)+tone(3000,rate,64./rate)*0.001

plotfft(numpy.hstack((t*numpy.kaiser(t.size,10),[0]*50000)),rate,0)