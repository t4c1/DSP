import numpy, scipy.io.wavfile,matplotlib.pyplot as plt, scipy.signal
from mysignal import play, tone
from correlation import normalize
responses={}
for n,el in enumerate(range(-40,91,10)):
    for az in range(0,181):
        try:
            rate,data=scipy.io.wavfile.read("KEMAR Compact\\elev%d\\H%de%03da.wav"%(el,el,az))
            responses[(el,az)]=normalize(1.0*data)
        except IOError:
            continue
        #print responses[el,az].shape,az,el

def get_response(el, az):
    absAz=abs(az)

    el0=int(el-el%10)
    for az0 in range(int(absAz), int(absAz-30), -1):
        if (el0,az0) in responses:
            break
    for az1 in range(int(absAz)+1, int(absAz+30)):
        if (el0,az1) in responses:
            break
    w1= (absAz - az0) / (az1 - az0)
    w0= (az1 - absAz) / (az1 - az0)
    tmp0=responses[el0,az0]*w0+responses[el0,az1]*w1
    el1=el0+10
    for az0 in range(int(absAz), int(absAz-30), -1):
        if (el1,az0) in responses:
            break
    for az1 in range(int(absAz)+1, int(absAz+30)):
        if (el1,az1) in responses:
            break
    w1= (absAz - az0) / (az1 - az0)
    w0= (az1 - absAz) / (az1 - az0)
    tmp1=responses[el1,az0]*w0+responses[el1,az1]*w1
    w1=(el-el0)/(el1-el0)
    w0=(el1-el)/(el1-el0)
    res = tmp0 * w0 + tmp1 * w1
    if az>=0:
        return res
    else:
        return numpy.vstack((res[:,1],res[:,0])).T

rate2,bee=scipy.io.wavfile.read("specific_sounds\\Misc\\Bee.wav")
bee=normalize(1.0*bee)
print responses[0,0].shape,get_response(-10,-10).shape,responses[0, 90][:, 0].shape,responses[0, 90][0,:].shape
print rate,rate2
tmp = numpy.vstack((
    numpy.vstack((bee,bee)).T,
    numpy.vstack((numpy.convolve(bee, responses[90, 0][:,0]), numpy.convolve(bee, responses[90, 0][:,1]))).T,
    numpy.vstack((numpy.convolve(bee, responses[0, 0][:,0]), numpy.convolve(bee, responses[0, 0][:,1]))).T,
))
play(tmp)
prec=10000000
#bee2=numpy.repeat(bee,int(float(prec)/bee.size+5))
#print bee2.shape,rate,rate2
res=numpy.zeros((prec,2))
for i in range(prec):
    t=i/float(prec)

    az=t*340-170
    el=0
    # az=0
    # el=t*100-30

    if (i%10000)==0:
        print i,el,az
    r=get_response(el,az)

    tmp = numpy.take(bee, numpy.arange(i, i + 128), mode="wrap")
    # res[i,:]=(tmp.dot(r[::-1, 0]),
    #           tmp.dot(r[::-1, 1]))
    res[i,:]=(tmp.dot(r[::-1, 0]),
              tmp.dot(r[::-1, 1]))
    # tmp = bee2[i:i + 128]
    # res[i,:]=(tmp.dot(r[::-1, 0]),
    #           tmp.dot(r[::-1, 1]))
play(res,rate2)

plt.plot(responses[-40,0][:,0],color="g")
plt.plot(responses[-40,0][:,1],color="r")
plt.show()


