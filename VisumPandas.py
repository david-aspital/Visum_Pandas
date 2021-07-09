import pandas as pd
import numpy as np
import os
import wx
import datetime
import time
import traceback

Visum = None
PRIO = 20480

def export_list(container, lla, path, name, filter=False):
    # Create Visum list and export it to the given path
    visum_list = None
    try:
        visum_list = eval(f'Visum.Lists.Create{}List',{'__builtins__':None},dispatcher)
    except:
        raise KeyError(f'"{container}" is not a valid Visum object.')
    visum_list.OpenLayout(lla)
    if filter:
        visum_list.SetObjects(filter)
    if name[-4:] == ".att":
        pass
    else:
        name = name+".att"
    visum_list.SaveToAttributeFile(f"{path}\\{name}",9)
    visum_list.Close()
    visum_list = None


def create_data_frame(list_type, layout, dir_name, temp_path, timeslice=None, filter=False):
    # Create pandas df from Visum list (export as att to temp path and read back)
    visum_list = None
    bkslsh = "\\"
    input_filename = layout.format(timeslice) if timeslice is not None else layout
    input_filepath = os.path.join(dir_name, input_filename)
    temp_file = f"{input_filename.replace('Inputs'+bkslsh,'')}.att"
    export_list(list_type, input_filepath, temp_path, temp_file, filter)
    data_frame = pd.read_csv(f"{temp_path}\\{temp_file}", sep="\t", header=2, skiprows=10)
    return data_frame