import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET

Visum = None
PRIO = 20480

def export_list(layout, folderpath, filename, filter=False):
    '''Create Visum list and export it to the given path\n
    .llax -> .att'''

    container = get_container(layout)
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


def create_data_frame(layout, folderpath, temp_path, timeslice=None, filter=False):
    '''Create pandas df from Visum list\n 
    Exports as .att to temp path and reads back as df\n
    .llax -> df'''
    visum_list = None
    bkslsh = "\\"
    filepath = os.path.join(folderpath, layout)
    temp_file = f"{layout}.att"
    export_list(filepath, temp_path, temp_file, filter)
    data_frame = pd.read_csv(os.path.join(temp_path, temp_file), sep="\t", header=2, skiprows=10)
    return data_frame

def get_container(llax):
    '''Get Visum object from .llax file\n
    .llax -> Visum container
    '''
    root = ET.parse(llax).getroot()
    for tag in root.findall('listLayoutCommonEntries'):
        obj = tag.get('layoutIdentifier').replace('LIST_LAYOUT_','')

    #TODO: Add dict that takes obj and returns the Visum container as they are not necessarily the same thing
    return obj