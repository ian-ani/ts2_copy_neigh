# PYTHON VERSION: 3.12.7

import os
import shutil
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog

# Asks user to choose a directory
def select_directory():
    root = Tk()
    root.withdraw()
    
    selected_directory = filedialog.askdirectory()
    parent = os.path.abspath(os.path.join(selected_directory, os.pardir))

    root.destroy()

    return parent, selected_directory

# Lists directories in destination folder
def ls_directory(directory):
    return os.listdir(directory)

# Folder number for renaming (ex. if N001 -> N001 but if N001 already exists then N001 -> N002)
def folder_number(directory, directory_name):
    for i in range(1, 999):
        number = directory_name[0]+"{:0>{}}".format(i, 3)
    
        if number not in directory:
            return number
        
# Copies folders from source to destination     
def copy_folder(source_directory, dest_directory, renamed_folder, list_directory):
    copied_folder = os.path.join(dest_directory, renamed_folder)
    
    # If it isn't in destination directory, then copy its folders
    if renamed_folder not in list_directory:
        shutil.copytree(source_directory, copied_folder)
    
# Creates path of destination folder and renamed folder (related to folder_number -> returns renamed_folder)
def create_path(dest_directory, renamed_folder): 
    return os.path.join(dest_directory, renamed_folder)

# Copies files...
def copy_file(entry, renamed_folder, directory):
    neighborhood_str_split = entry.name.split("_")
    neighborhood_str_split[0] = renamed_folder
    neighborhood_name_result = "_".join(neighborhood_str_split)

    origin_file_copy_path = os.path.join(directory, entry.name)
    dest_file_copy_path = os.path.join(directory, neighborhood_name_result)

    shutil.move(origin_file_copy_path, dest_file_copy_path)

# ...while it renames them
def rename_file(directory, renamed_folder):  
    for folder in os.scandir(directory):
        # Copies and renames files inside root directory
        if folder.is_file():
            for entry in os.scandir(directory):
                if entry.is_file():
                    copy_file(entry, renamed_folder, directory)
        # Copies and renames files of subdirectories
        elif Path(folder).is_dir() and folder.name != "Storytelling":
            folder_path = os.path.join(directory, folder.name)
            for entry in os.scandir(os.path.join(directory, folder.name)):
                if entry.is_file():
                    copy_file(entry, renamed_folder, folder_path)
