# PYTHON VERSION: 3.12.7

import os.path
import tkinter as tk
from tkinter import PhotoImage
from tkinter.messagebox import askyesno
import webbrowser
import json

import core
import utils.utiles as util
import constants as c
from utils.utiles import resource_path

class App:

    # Logger
    log = ""
    lines = 0
    
    # App icon
    icon = resource_path(os.path.join("utils", "icon.ico"))

    def __init__(self):
        # UI texts
        path_dict = resource_path(os.path.join("language", "lang_dict.json"))
        with open(path_dict, "r", encoding="utf-8") as f:
                lang_dict = json.load(f)

        self.lang_dict_en = lang_dict["lang_dict_en"]
        self.lang_dict_es = lang_dict["lang_dict_es"]

        # Project directory (src)
        self.PY_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

        # Directories
        self.source_directory = None
        self.dest_directory = None

        # Default language
        self.ui_text = self.lang_dict_en

        # Help files paths
        self.help_url = {
            "es": os.path.join(self.PY_FILE_PATH, "help", "ayuda.html"),
            "en": os.path.join(self.PY_FILE_PATH, "help", "help.html")
        }

        # Setups
        self.setup_main_window()
        self.setup_buttons()
        self.setup_logger()
        self.create_log()
  
    # Main window
    def setup_main_window(self):
        self.main_window = tk.Tk()
        self.main_window.iconbitmap(True, self.icon)
        self.main_window.geometry(c.WINDOW_GEOMETRY)
        self.main_window.title(self.ui_text["title"])
        self.main_window.configure(bg=c.WINDOW_BG_COLOR)
        self.main_window.resizable(False, False)

    # Buttons
    def setup_buttons(self):
        self.source_main_window = util.get_button(self.main_window, self.ui_text["source_directory"], c.BUTTON_COLOR[0], 
                                                  lambda: self.path_button("selected_source_message", "source_directory"))
        self.source_main_window.place(x=c.START_X, y=c.START_Y[0])

        self.dest_main_window = util.get_button(self.main_window, self.ui_text["dest_directory"], c.BUTTON_COLOR[0], 
                                                lambda: self.path_button("selected_destination_message", "dest_directory"))
        self.dest_main_window.place(x=c.START_X, y=c.START_Y[0] + c.STEP_Y)

        self.run_main_window = util.get_button(self.main_window, self.ui_text["run"], c.BUTTON_COLOR[1], self.run_button)
        self.run_main_window.config(state=tk.DISABLED)
        self.run_main_window.place(x=c.START_X, y=c.START_Y[0] + c.STEP_Y * 2)

        self.language_main_window = util.get_button(self.main_window, self.ui_text["language"], c.BUTTON_COLOR[2], self.change_language)
        self.language_main_window.place(x=c.START_X, y=c.START_Y[1])

        self.help_main_window = util.get_button(self.main_window, self.ui_text["help"], c.BUTTON_COLOR[2], self.help_button)
        self.help_main_window.place(x=c.START_X, y=c.START_Y[1] + c.STEP_Y)

    # Logger
    def setup_logger(self):
        self.label_border = tk.Frame(self.main_window, bg=c.LOGGER_BORDER_COLOR, relief="sunken", bd=2)
        self.label_text = tk.Label(self.label_border, font=(c.FONT_FAMILY, c.FONT_SIZE), justify="left", anchor="nw", width=c.LOGGER_WIDTH, 
                                   height=c.LOGGER_HEIGHT, bg=c.FONT_BG_COLOR, fg=c.FONT_COLOR)
        self.label_text.pack(fill="both", expand=True, padx=1, pady=1)
        self.label_border.pack(anchor="nw", padx=c.PADDING, pady=c.PADDING)

    # Get source and destination directories
    def path_button(self, key, prueba):
        parent_directory, self.directory = core.select_directory()

        setattr(self, prueba, self.directory)
        self.write_log(key, directory=getattr(self, prueba))

        self.switch_state()

    # Main logic
    def run_button(self):
        answer_execute = askyesno(self.ui_text["run"], self.ui_text["checking"])

        if answer_execute:
            self.write_log("start_copy_message", dest_directory=self.dest_directory)
            list_directory = core.ls_directory(self.dest_directory)
            self.write_log("directory_list_message", list_directory=list_directory if len(list_directory) != 0 else "it is is empty")
            directory_name = os.path.basename(self.source_directory)
            self.write_log("copying_message", directory_name=directory_name)
            renamed_folder = core.folder_number(list_directory, directory_name)
            self.write_log("start_rename_message", directory_name=directory_name, renamed_folder=renamed_folder)
            core.copy_folder(self.source_directory, self.dest_directory, renamed_folder, list_directory)
            core.ls_directory(self.dest_directory)
            full_path = core.create_path(self.dest_directory, renamed_folder)
            self.write_log("renaming_message")
            core.rename_file(full_path, renamed_folder)
            self.write_log("finished_message")

    # Blocked until both directories have been selected
    def switch_state(self):
        if not self.source_directory or not self.dest_directory:
            self.run_main_window.config(state=tk.DISABLED)
        else:
            self.run_main_window.config(state=tk.NORMAL)

    # Changes language
    def change_language(self):
        if self.ui_text == self.lang_dict_es:
            self.ui_text = self.lang_dict_en
        else:
            self.ui_text = self.lang_dict_es

        self.main_window.title(self.ui_text["title"])
        self.source_main_window.config(text=self.ui_text["source_directory"])
        self.dest_main_window.config(text=self.ui_text["dest_directory"])
        self.run_main_window.config(text=self.ui_text["run"])
        self.language_main_window.config(text=self.ui_text["language"])
        self.help_main_window.config(text=self.ui_text["help"])

    # Help button
    def help_button(self):
        if self.ui_text == self.lang_dict_es:
            webbrowser.open("file://" + self.help_url["es"])
        else:
            webbrowser.open("file://" + self.help_url["en"])

    # Logger
    def create_log(self):
        self.label_text.config(text=self.log)
        self.main_window.after(1000, self.create_log)

    def write_log(self, message, **kwargs):
        if self.lines == c.MAX_NUM_LINES:
            self.clean_log()
            self.lines = 0
        
        try:
            self.log += self.ui_text[message].format(**kwargs)+"\n"
        except KeyError as e:
            raise KeyError(f"Something went wrong, does the given key exist? {e}")
        self.lines += 1

    def clean_log(self):
        self.log = ""
            
    # Closes program
    def exit_button(self):
        answer = askyesno(self.ui_text["exit"], self.ui_text["checking"])

        if answer:
            self.main_window.destroy()

    # Starts program
    def start(self):
        self.main_window.protocol("WM_DELETE_WINDOW", self.exit_button)
        self.main_window.mainloop()
