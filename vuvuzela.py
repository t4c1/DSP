import numpy,scipy.io.wavfile
from iir import make_filter,plot_filter_response
from mysignal import play
from freqencyAnalysis import plotfft
vuvufreqs=[236,472,708,943,1181, 1413]
#sampling_freq=44100


sampling_freq,v=scipy.io.wavfile.read("Vuvuzela_single_note_govor.wav")
#sampling_freq,v=scipy.io.wavfile.read("Vuvuzela_single_note.wav")
print sampling_freq

zeroes=[]
poles=[]
poledist=0.992

for freq in vuvufreqs:
    direction=numpy.e**(1j*numpy.pi*float(freq)/sampling_freq*2)
    d2=numpy.conj(direction)
    zeroes.append(direction)
    zeroes.append(d2)
    poles.append(direction*poledist)
    poles.append(d2*poledist)

fil=make_filter(zeroes, poles)
plot_filter_response(fil, sampling_freq, 4096, True)

#plotfft(v[:,0],sampling_freq,True)
#plotfft(fil(v[:,0]),sampling_freq,True)
#plotfft(fil(fil(v[:,0])),sampling_freq,True)

play(fil(fil(v[:,0])))