from os.path import isfile,join
from os import listdir
import matplotlib.pyplot as plt, numpy as np
from read import read_np

LABEL_DIR = "../labels"
DATA_DIR = "../data"

data_files = [f for f in listdir(LABEL_DIR) if isfile(join(LABEL_DIR, f))]
print(data_files)

rad = 0.69/2
per = 2*3.14159*rad

def process(x):
    line = x.strip().split(",")
    #time, val, index
    return (float(line[0]),float(line[1]),int(line[2]))



plt.figure()
for fp in data_files:
    with open(join(LABEL_DIR,fp)) as f:
        labels = f.readlines()
        labels = [process(x) for x in labels]
    signal = read_np(fp.split(".")[0]+".csv", DATA_DIR)
    amps = []
    T = []  
    for i in range(len(labels)-1):
        x1,y1,ix1 = labels[i]
        x2,y2,ix2 = labels[i+1]
        amps.append(np.mean(np.abs(signal[ix1:ix2+1, 1])))
        T.append(x2-x1)
    V = [per/t*3.6 for t in T]
    IT = [1/t for t in T]
    plt.scatter(V, amps)

# plt.title("fp: "+fp)
plt.xlabel("Vitesse au sol(km/h)")
plt.ylabel("Amplitude sur Tour")
plt.tight_layout()
plt.show()
