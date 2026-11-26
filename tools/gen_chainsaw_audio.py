"""Synthesize original mono chainsaw motor/contact effects. Requires soundfile + numpy.
No sampled recordings or third-party audio are used. Run python tools/gen_chainsaw_audio.py.
"""
from pathlib import Path
import math, random
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]/'src/main/resources/assets/fpe/sounds/zombie_au'
ROOT.mkdir(parents=True,exist_ok=True)
SR=22050

def engine():
    rng=random.Random(829);phase=0;low=0;out=[]
    for i in range(int(.60*SR)):
        t=i/SR;freq=105+35*(1-math.exp(-t*18))+5*math.sin(t*math.tau*8)
        phase+=math.tau*freq/SR
        pulse=sum(math.sin(phase*h)/h**.7 for h in range(1,13))
        noise=rng.uniform(-1,1);low=.91*low+.09*noise
        teeth=(noise-low)*(.32+.18*math.sin(phase*3))
        env=min(1,t/.012,(.60-t)/.035)
        out.append(.72*math.tanh((.65*pulse+teeth)*1.15)*max(0,env))
    return out

def cut():
    rng=random.Random(611);out=[];old=0
    for i in range(int(.19*SR)):
        t=i/SR;n=rng.uniform(-1,1);h=n-old*.72;old=n
        env=min(1,t/.004)*math.exp(-t*19)
        out.append(.65*math.tanh(1.3*h+.3*math.sin(t*math.tau*380))*env)
    return out

if __name__=='__main__':
    for name,data in [('chainsaw_engine',engine()),('chainsaw_cut',cut())]:
        sf.write(ROOT/(name+'.ogg'),data,SR,format='OGG',subtype='VORBIS')
        assert max(abs(x) for x in data)<1
        print(name,len(data)/SR,'seconds, peak',round(max(abs(x) for x in data),3))
