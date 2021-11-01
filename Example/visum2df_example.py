import pandas as pd
import numpy as np
import os
import tempfile
import datetime


def export_list(layout, filename=None, folderpath=None):
    '''Export list to the given path as attribute file

    Parameters
    ----------
    layout : str
        The layout file name (incuding extension). If no extension is provided, .llax will be assumed.
    filename : str, path object, optional
        The filename of the exported .att file. By default it is the same as the name of the .llax file.
    folderpath : str, path object, optional
        The folder path of the export location. By default it is the same folder as the Visum .ver file
    '''
    if filename is None:
        filename = layout

    if folderpath is None:
        folderpath = os.path.dirname(Visum.IO.CurrentVersionFile)

    name, ext = os.path.splitext(layout)
    if not (ext == '.llax' or ext == '.lla'):
        layout += '.llax'

    name, ext = os.path.splitext(filename)
    if ext != 'att':
        name += '.att'
    
    Visum.IO.SaveAttributeFile(os.path.join(folderpath, name), layout, 9)


def create_data_frame(visum_list=None, layout=None, temp_path=tempfile.gettempdir(), folderpath=None):
    '''Create pandas df from Visum list by exporting as .att to temp path and reading back as df

    Parameters
    ----------
    visum_list : obj, optional
        The Visum list object (including all columns to be exported). Either layout or this variable needs to be provided.
    layout : str, optional
        The layout file name (incuding extension). If no extension is provided, .llax will be assumed. Either visum_list or this variable needs to be provided.
    temp_path : str, path object, optional
        The folder path of the temporary location to write attribute data to. By default this is the %TMP% location
    folderpath : str, path object, optional
        The folder path of the layout file. By default it is the same folder as the Visum .ver file

    Returns
    ----------
    DataFrame
    '''

    if (visum_list is None) and (layout is None):
        raise ValueError("Either visum_list or layout need to be defined.")

    if folderpath is None:
        folderpath = os.path.dirname(Visum.IO.CurrentVersionFile)

    if not (layout is None):
        name, ext = os.path.splitext(layout)
        if not (ext == '.llax' or ext == '.lla'):
            layout += '.llax'
        filepath = os.path.join(folderpath, layout)
        temp_file = f"{name}.att"
        export_list(filepath, temp_file, temp_path)
    else:
        temp_file = f'visum_list_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.att'
        visum_list.SaveToAttributeFile(os.path.join(temp_path, temp_file), 9)
    data_frame = pd.read_csv(os.path.join(temp_path, temp_file), sep="\t", header=2, skiprows=10)
    return data_frame


if __name__ == '__main__':
    temp_path = tempfile.gettempdir()

    # Include .llax extension, temp path location and folderpath of llax
    node_df = create_data_frame('Nodes.llax', temp_path, os.path.curdir)
    # Miss extension from layout file
    aqd_df = create_data_frame('QualityData', temp_path, os.path.curdir)
    # Miss temp_path and folderpath arguments as well as layout extension
    paths_df = create_data_frame('PrTPaths')
    # Need to include extension for .lla files
    link_df = create_data_frame('Links.lla')
    # Subfolders can be used - either relative to the version file (as here) or absolute path
    turns_in_df = create_data_frame('TurnInput.llax', folderpath='Layouts')
    # Can export the .att file elsewhere if required
    turns_out_df = create_data_frame('TurnOutput', temp_path='Exports')