import shutil
from os.path import join, isfile, isdir
import os

DATA_ROOT = "../"
DATA_OUT = join(DATA_ROOT, "data")
DEFAULT_SEP = ","
DEFAULT_DEC = "."
SOURCES = [
    {"name":"data_oscillo",
     "date":"dec 16 2024",
     "description":"premieres mesures, problemes de déclenchement",
     "columns":["T", "V1", "V2"],
     "sep":",",
     "dec":".",
    #  "to_numpy":read_np,
    },
    {"name":"data_sysam",
     "date":"jan 6 2025",
     "description":"mesures de test sur une carte d'acquisition du lycée",
     "columns":["T", "V1"],
     "sep":";",
     "dec":",",
    #  "to_numpy":read_np_sysam,
    }
]

def read_generator(path, rows_2_skip=0, sep=",", dec="."):
    with open(path, "r", encoding="utf-8") as file:
        i = 0
        while (line := file.readline())!="":
            x = line.strip().split(sep)
            if "" not in x:
                try:
                    yield tuple(map(lambda x: float(x.replace(dec,".")),x))
                except:
                    pass
            i+=1

#list all files within DATA_ROOT / source["name"] and copy them to DATA_OUT using the generator to discard useless lines
for source in SOURCES:
    dirpath = join(DATA_ROOT, source["name"])
    if not isdir(dirpath):
        print(f"WARNING: DIR {dirpath} MISSING")
        continue
    for f in os.listdir(dirpath):
        if f.strip().split(".")[-1] not in ["csv"]:
            print(f"WARNING: skipping non-csv {f}")
            continue
        fp = join(dirpath,f)
        if not isfile(fp):
            print(f"WARNING: skipping non-file {fp}")
            continue
        print(f"-> Converting {fp}...")
        generator = read_generator(fp, sep=source.get("sep", DEFAULT_SEP), dec=source.get("dec", DEFAULT_DEC))
        writepath = join(DATA_OUT,f)
        if os.path.exists(writepath):
            # os.remove(writepath)
            pass
        with open(writepath, "w") as file:
            #write header with column names
            file.write(",".join(source["columns"])+"\n")
            for line in generator:
                file.write(",".join(map(str,line))+"\n")




# from os.path import join, isfile, isdir
# import os
# import csv
# import numpy as np


# def read_np(path, rows_2_skip=2):
#     with open(path, "r", encoding="utf-8") as f:
#         lines = f.readlines()
#     lines =[list(map(float, z)) for x in lines[rows_2_skip:] if (y:=x.strip())!="" and (not "" in (z:=y.split(",")))] #discard unrecorded values
#     return np.array(lines)

# def read_np_sysam(paths, rows_2_skip=1):
#     with open(path, "r", encoding="utf-8") as f:
#         lines = f.readlines()
#     lines =[list(map(float, z)) for x in lines[rows_2_skip:] if (y:=x.strip())!="" and (not "" in (z:=y.split(",")))] #discard unrecorded values
#     return np.array(lines)

# def checkvalid(source):
#     if not isdir(dirpath):
#         print(f"WARNING: DIR {dirpath} MISSING")
#         return False
#     if not "to_numpy" in source:
#         print("WARNING: missing conversion function")
#         return False
#     return True



# print("Normalisation des formats de fichier...")

# for source in SOURCES:
#     dirpath = join(DATA_ROOT, source["name"])
#     print(f"Converting {dirpath}")
#     if not checkvalid(source):
#         continue
    
#     extensions = source.get("extensions", None)
#     if extensions is None:
#         print("Filtering by csv by default.")
#         extensions = ["csv"]
    
#     filenames = [] #file names ending with their format: "gcope22.csv"
#     filepaths = [] #paths to the corresponding files
#     for f in os.listdir(dirpath):
#         fp = join(dirpath,f)
#         if isfile(fp) and f.strip().split(".")[-1] in extensions:
#             filenames.append(f)
#             filepaths.append(fp)
#     for name, path in zip(filenames,filepaths):
#         array = dirpath["to_numpy"](path)
#         writepath = join(DATA_OUT,name)
#         if os.path.exists(writepath):
#             os.remove(writepath)
#         with open(writepath, "wb") as file:
#             writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             writer.writerows
