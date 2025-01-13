import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join

DATDIR = "data"

def read_dat(file_name, dat_dir=DATDIR):
    path = join(dat_dir, file_name)    
    df = pd.read_csv(path, sep=",", skiprows=[1], dtype=np.float64)
    df = df.drop(0)
    df = df.dropna(subset=["1", "2"])
    df = df.rename(columns={"x-axis": "Time", "1": "S1", "2": "S2"})
    return df

def read_np(file_name, dat_dir=DATDIR, rows_skip=1):
    path = join(dat_dir, file_name)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines =[list(map(float, z)) for x in lines[rows_skip:] if (y:=x.strip())!="" and (not "" in (z:=y.split(",")))]
    return np.array(lines)


if __name__=="__main__":
    pass
    # print(df)
    # input()
    # plt.figure()
    # plt.plot(df["Time"], df["S1"], label="raw")
    # # plt.legend()
    # plt.savefig("fig.png")

