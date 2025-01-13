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
NAMES_INDEX = ["mesure_proche", "mesure_loin", "mesure_med"]

def process(x):
    line = x.strip().split(",")
    #time, val, index
    return (float(line[0]),float(line[1]),int(line[2]))

def get_index(fp):
    index = 0
    for i in range(len(NAMES_INDEX)):
        if NAMES_INDEX[i] in fp:
            index = i+1
            break
    return index

ampl_mesures = [[] for i in range(len(NAMES_INDEX))]
temps_mesures = [[] for i in range(len(NAMES_INDEX))]
V_mesures = [[] for i in range(len(NAMES_INDEX))]
Vmax = None

plt.figure()
for fp in data_files:
    idx = get_index(fp)
    print(fp, idx)
    if idx == 0:
        continue
    idx-=1
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
        ampl_mesures[idx].append(calculatedAmp)
        temps_mesures[idx].append(x2-x1)
        localV = PERIMETRE_ROUE/(x2-x1)*3.6
        V_mesures[idx].append(localV)
        if Vmax is None or localV > Vmax:
            Vmax = localV

toffset = 4
Vmin = -toffset
Vmax+= toffset

for i in range(len(NAMES_INDEX)):
    plt.scatter(V_mesures[i], ampl_mesures[i], label=NAMES_INDEX[i])
    reg = stats.linregress(V_mesures[i], ampl_mesures[i])

    valsT = [Vmin, Vmax]
    valsL = [reg[1]+Vmin*reg[0], reg[1] + Vmax*reg[0]]
    plt.plot(valsT,valsL)

# plt.title("fp: "+fp)
plt.xlabel("Vitesse au sol(km/h)")
plt.ylabel("abs(V) moyen sur tour")
plt.grid()
plt.tight_layout()
plt.legend()
plt.show()

#now perform an fft on each signal between mintime and maxtime of each label series
#and plot the results
plt.clf()
plt.figure()
for ix_to_test in range(len(NAMES_INDEX)):
    plt.subplot(len(NAMES_INDEX), 1, ix_to_test+1)
    filepaths = list(filter(lambda x: get_index(x)-1 == ix_to_test, data_files))
    file_count = len(filepaths)
    for i,fp in enumerate(filepaths):

        with open(join(LABEL_DIR,fp)) as f:
            labels = f.readlines()
            labels = [process(x) for x in labels]
        minidx = labels[0][2]
        maxidx = labels[-1][2]
        nametag = fp.split(".")[0]
        signal = read_np(nametag+".csv", DATA_DIR)

        #figure out the time interval
        mintime = labels[0][0]
        maxtime = labels[-1][0]
        N = len(signal)
        T = (maxtime - mintime)/(N-1)
        #exctract values within the first and last label
        values = signal[minidx:maxidx+1]
        #perform the fft
        fft_values = np.fft.fft(values[:,1])
        freqs = np.fft.fftfreq(len(values[:,1]), T)
        #plot the results
        plt.plot(freqs, np.abs(fft_values))
    plt.title("fp: "+fp)
plt.show()
