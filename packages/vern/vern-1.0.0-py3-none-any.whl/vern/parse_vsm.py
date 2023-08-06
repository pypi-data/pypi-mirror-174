# profilometer
import numpy as np
import pandas as pd
from misc import *

def read_files(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()
        
    df = pd_read_csv(
        filename=input_path, encoding="cp932", sep=",", header_count=28, 
        names_old=["magnetic field (Oe)", "magnetization (erg/cm^3)"], names_new=["magnetic field (Oe)", "magnetization (erg/cm^3)"], unit_conversion_coefficients=[1, 1]
    )
    df.to_csv(output_path, index=False)

def main(**kwargs):
    read_files(kwargs["input_path"], kwargs["output_path"])
