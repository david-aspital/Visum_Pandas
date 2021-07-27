import pandas as pd
import numpy as np
import os

Visum = None

def export_list(layout, folderpath, filename):
    '''Export list to the given path as attribute file\n
    .llax -> .att'''

    if filename[-4:] != ".att":
        filename = filename+".att"
    Visum.IO.SaveAttributeFile(os.path.join(folderpath, filename), layout, 9)


def create_data_frame(layout, folderpath, temp_path):
    '''Create pandas df from Visum list\n 
    Exports as .att to temp path and reads back as df\n
    .llax -> df'''
    filepath = os.path.join(folderpath, layout)
    temp_file = f"{layout}.att"
    export_list(filepath, temp_path, temp_file)
    data_frame = pd.read_csv(os.path.join(temp_path, temp_file), sep="\t", header=2, skiprows=10)
    return data_frame
