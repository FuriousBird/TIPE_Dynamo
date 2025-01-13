from read import read_dat
import os
import matplotlib.pyplot as plt

DATA_DIR = "data"
SYSAM_DATA_DIR = "data_sysam"
VIZ_DIR = "viz"
SYSAM_VIZ_DIR = "viz_sysam"

filter = lambda x: x.endswith(".csv")
files = [x for x in os.listdir(DATA_DIR) if filter(x) and os.path.isfile(os.path.join(DATA_DIR, x))]
print(files)

for filename in files:
    rawname = filename.split(".")[0]
    df = read_dat(filename, dat_dir=DATA_DIR)
    plt.figure()
    plt.plot(df["Time"], df["S1"])
    plt.savefig(os.path.join(VIZ_DIR, rawname+".jpg"))
    if "gcope_24" in rawname or False:
        plt.show()

files = [x for x in os.listdir(SYSAM_DATA_DIR) if filter(x) and os.path.isfile(os.path.join(SYSAM_DATA_DIR, x))]
print(files)

for filename in files:
    rawname = filename.split(".")[0]
    df = read_dat(filename, dat_dir=SYSAM_DATA_DIR, sep=";", decimal=",", dropna=False)
    plt.figure()
    plt.plot(df["Temps"], df["V1"])
    plt.savefig(os.path.join(SYSAM_VIZ_DIR, rawname+".jpg"))
    
    plt.show()