import pandas as pd
import numpy as np
import os

Visum = None
PRIO = 20480

def export_list(container, layout, folderpath, filename, filter=False):
    # Create Visum list and export it to the given path
    visum_list = None
    try:
        visum_list = eval(f'Visum.Lists.Create{container}List',{'__builtins__':None})
    except:
        raise KeyError(f'"{container}" is not a valid Visum object.')
    visum_list.OpenLayout(layout)
    if filter:
        visum_list.SetObjects(filter)
    if filename[-4:] != ".att":
        filename = filename+".att"
    visum_list.SaveToAttributeFile(os.path.join(folderpath, filename),9)
    visum_list.Close()
    visum_list = None


def create_data_frame(container, layout, folderpath, temp_path, timeslice=None, filter=False):
    # Create pandas df from Visum list (export as att to temp path and read back)
    visum_list = None
    bkslsh = "\\"
    filepath = os.path.join(folderpath, layout)
    temp_file = f"{layout}.att"
    export_list(container, filepath, temp_path, temp_file, filter)
    data_frame = pd.read_csv(os.path.join(temp_path, temp_file), sep="\t", header=2, skiprows=10)
    return data_frame

