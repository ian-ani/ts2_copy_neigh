# PYTHON VERSION: 3.11.9

import os
import shutil
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog

def select_directory():
    root = Tk()
    root.withdraw()
    
    selected_directory = filedialog.askdirectory()
    parent = os.path.abspath(os.path.join(selected_directory, os.pardir))

    root.destroy()

    return parent, selected_directory

def ls_directory(directory):
    folders = os.listdir(directory)
    
    return folders

def folder_number(directory, _directory_name):
    for i in range(1, 999):
        number_str = _directory_name[0]+"{:0>{}}".format(i, 3)
    
        if number_str not in directory:
            return number_str
        
def copy_folder(_origin_directory, _dest_directory, _renamed_folder, _list_directory):
    copied_folder = os.path.join(_dest_directory, _renamed_folder)
    
    if _renamed_folder not in _list_directory:
        shutil.copytree(_origin_directory, copied_folder)
    else:
        pass
    
def create_paths(_dest_directory, _renamed_folder):
    
    full_path = os.path.join(_dest_directory, _renamed_folder)
    
    return full_path

def rename_files(directory, _renamed_folder):   
    for folder in os.scandir(directory):
        if Path(folder).is_dir() and folder.name != "Storytelling":
            folder_path = os.path.join(directory, folder.name)
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    neighborhood_str_split = entry.name.split("_")
                    neighborhood_str_split[0] = _renamed_folder
                    neighborhood_name_result = "_".join(neighborhood_str_split)
    
                    origin_file_copy_path = os.path.join(folder_path, entry.name)
                    dest_file_copy_path = os.path.join(folder_path, neighborhood_name_result)
    
                    shutil.move(origin_file_copy_path, dest_file_copy_path)
        elif folder.is_file():
            for entry in os.scandir(directory):
                if entry.is_file():
                    neighborhood_str_split = entry.name.split("_")
                    neighborhood_str_split[0] = _renamed_folder
                    neighborhood_name_result = "_".join(neighborhood_str_split)
    
                    origin_file_copy_path = os.path.join(directory, entry.name)
                    dest_file_copy_path = os.path.join(directory, neighborhood_name_result)
    
                    shutil.move(origin_file_copy_path, dest_file_copy_path)
