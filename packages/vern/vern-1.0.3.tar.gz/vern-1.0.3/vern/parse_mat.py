# profilometer
import numpy as np
import pandas as pd
from misc import *
import mat73

def read_files(input_path, txt_path):
    mat = mat73.loadmat(input_path)
    df = pd.DataFrame.from_dict(mat)
    df.to_csv(txt_path, index=False)

def main(**kwargs):
    read_files(kwargs["input_path"], kwargs["txt_path"])
