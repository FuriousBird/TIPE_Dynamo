from read import read_dat
import os
import matplotlib.pyplot as plt

DATA_DIR = "data"
VIZ_DIR = "viz"

filter = lambda x: x.endswith(".csv")
files = [x for x in os.listdir(DATA_DIR) if filter(x) and os.path.isfile(os.path.join(DATA_DIR, x))]
print(files)

for filename in files:
    rawname = filename.split(".")[0]
    df = read_dat(filename, dat_dir=DATA_DIR)
    plt.figure()
    plt.plot(df["Time"], df["S1"])
    plt.savefig(os.path.join(VIZ_DIR, rawname+".jpg"))
    if "gcope_24" in rawname:
        plt.show()