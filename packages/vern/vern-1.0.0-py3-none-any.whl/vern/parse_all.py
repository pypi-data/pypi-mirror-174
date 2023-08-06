# profilometer
import os
import parse_dxf
import parse_oscilloscope
import parse_profilometer
import parse_tabular
import parse_vsm
import parse_mat
from misc import *
#import parse_pptx

def read_files(**kwargs):
    with open(kwargs["input_path"], "r") as f:
        try:
            lines = f.readlines()
        except:
            lines = None

    if ".mat" in kwargs["input_filename"] or "_m.MAT" in kwargs["input_filename"]: # convert .mat to tabular data
        parse_mat.main(**kwargs)
    elif "_m1.txt" in kwargs["input_filename"] or "_m1.TXT" in kwargs["input_filename"]: # manual plot with tabular data and linear regression
        parse_tabular.main(**kwargs, linear_regression=True)
    elif "_m.txt" in kwargs["input_filename"] or "_m.TXT" in kwargs["input_filename"]: # manual plot with tabular data
        parse_tabular.main(**kwargs)
    elif "_i.txt" in kwargs["input_filename"] or "_i.TXT" in kwargs["input_filename"]: # profilometer
        parse_profilometer.main(**kwargs, interactive=True)
    elif ".txt" in kwargs["input_filename"] or ".TXT" in kwargs["input_filename"]: # profilometer
        parse_profilometer.main(**kwargs)
    elif ".Dat" in kwargs["input_filename"]: # VSM
        parse_vsm.main(**kwargs)
    #elif ".pptx" in filename or ".PPTX" in filename: # pptx
    #    parse_pptx.main(**kwargs)
    elif ".dxf" in kwargs["input_filename"] or ".DXF" in kwargs["input_filename"]: # autocad DXF
        parse_dxf.main(**kwargs)
    elif "DL9000" in lines[1]: # oscilloscope_electrical
        parse_oscilloscope.main(**kwargs)

class rrn():
    def __init__(input_path):
        input_directory = os.path.dirname(input_path)
        input_filename = os.path.basename(input_path)
        input_filename_wo_ext = os.path.splitext(input_filename)[0]

        txt_directory = input_directory
        txt_filename_wo_ext = input_filename_wo_ext
        txt_filename = txt_filename_wo_ext + ".txt"
        txt_path = os.path.join(txt_directory, txt_filename)

        csv_directory = os.path.join(input_directory, "report")
        csv_filename_wo_ext = input_filename_wo_ext
        csv_filename = csv_filename_wo_ext + ".csv"
        csv_path = os.path.join(csv_directory, csv_filename)

        plot_directory = os.path.join(input_directory, "report")
        plot_filename_wo_ext = input_filename_wo_ext
        plot_filename = plot_filename_wo_ext + ".png"
        plot_path = os.path.join(plot_directory, plot_filename)

        hist_directory = os.path.join(input_directory, "report")
        hist_filename_wo_ext = input_filename_wo_ext + "_hist"
        hist_filename = hist_filename_wo_ext + ".png"
        hist_path = os.path.join(hist_directory, hist_filename)

        svg_directory = os.path.join(input_directory, "report")
        svg_filename_wo_ext = input_filename_wo_ext
        svg_filename = svg_filename_wo_ext + ".svg"
        svg_path = os.path.join(svg_directory, svg_filename)

        for directory in [csv_directory, plot_directory, svg_directory]:
            if not os.path.isdir(directory):
                os.mkdir(directory)
                
        read_files(**{
            "input_path":            input_path,
            "input_directory":       input_directory,
            "input_filename":        input_filename,
            "input_filename_wo_ext": input_filename_wo_ext,

            "txt_path":            txt_path,
            "txt_directory":       txt_directory,
            "txt_filename":        txt_filename,
            "txt_filename_wo_ext": txt_filename_wo_ext,

            "csv_path":            csv_path,
            "csv_directory":       csv_directory,
            "csv_filename":        csv_filename,
            "csv_filename_wo_ext": csv_filename_wo_ext,

            "plot_path":            plot_path,
            "plot_directory":       plot_directory,
            "plot_filename":        plot_filename,
            "plot_filename_wo_ext": plot_filename_wo_ext,

            "hist_path":            hist_path,
            "hist_directory":       hist_directory,
            "hist_filename":        hist_filename,
            "hist_filename_wo_ext": hist_filename_wo_ext,

            "svg_path":            svg_path,
            "svg_directory":       svg_directory,
            "svg_filename":        svg_filename,
            "svg_filename_wo_ext": svg_filename_wo_ext,
        })