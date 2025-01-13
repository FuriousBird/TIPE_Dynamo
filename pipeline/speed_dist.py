from os.path import isfile,join
from os import listdir
import matplotlib.pyplot as plt, numpy as np
from read import read_np
import scipy.stats as stats

LABEL_DIR = "../labels"
DATA_DIR = "../data"

data_files = [f for f in listdir(LABEL_DIR) if isfile(join(LABEL_DIR, f))]
print(data_files)

RAYON_ROUE = 0.69/2
PERIMETRE_ROUE = 2*3.14159*RAYON_ROUE

def process(x):
    line = x.strip().split(",")
    #time, val, index
    return (float(line[0]),float(line[1]),int(line[2]))

proches = []
temps_proches = []

loins = []
temps_loins = []

plt.figure()
for fp in data_files:
    ispro, isloin = "mesure_proche" in fp, "mesure_loin" in fp
    if not(ispro or isloin):
        continue
    with open(join(LABEL_DIR,fp)) as f:
        labels = f.readlines()
        labels = [process(x) for x in labels]
    nametag = fp.split(".")[0]
    signal = read_np(nametag+".csv", DATA_DIR)
    amps = []
    T = []  
    for i in range(len(labels)-1):
        x1,y1,ix1 = labels[i]
        x2,y2,ix2 = labels[i+1]
        calculatedAmp = 0.5*np.mean(np.abs(signal[ix1:ix2+1, 1]))
        amps.append(calculatedAmp)
        T.append(x2-x1)
        if ispro:
            proches.append(calculatedAmp)
            temps_proches.append(x2-x1)
        if isloin:
            loins.append(calculatedAmp)
            temps_loins.append(x2-x1)

    V = [PERIMETRE_ROUE/t*3.6 for t in T]
    IT = [1/t for t in T]
Vl = [PERIMETRE_ROUE/t*3.6 for t in temps_loins]
Vp = [PERIMETRE_ROUE/t*3.6 for t in temps_proches]
plt.scatter(Vp, proches, label="proches")
plt.scatter(Vl, loins, label="loins")

tmax = max(np.max(Vl), np.max(Vp))
rl = stats.linregress(Vl, loins)
rp = stats.linregress(Vp, proches)
valsT = [0, tmax]
valsL = [rl[1], rl[1] + tmax*rl[0]]
valsP = [rp[1], rp[1] + tmax*rp[0]]

plt.plot(valsT,valsL)
plt.plot(valsT,valsP)

# plt.title("fp: "+fp)
plt.xlabel("Vitesse au sol(km/h)")
plt.ylabel("Amplitude sur Tour")
plt.tight_layout()
plt.legend()
plt.show()
