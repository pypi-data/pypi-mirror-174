# profilometer
import numpy as np
import pandas as pd
from misc import *

def read_files(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()

    df = pd_read_csv( 
        filename=input_path, encoding="utf-8", sep=",", header_count=16, 
        names_old=["erase1", "Voltage (V)", "erase2"], names_new=["erase1", "Voltage (V)", "erase2"], unit_conversion_coefficients=[1, 1, 1], 
        use_index=True, name_index="time (ns)", index_coefficient=4E-013*1e9
    )
    df.to_csv(output_path, index=False)
    plot(df)

def main(**kwargs):
    read_files(kwargs["input_path"], kwargs["output_path"])
