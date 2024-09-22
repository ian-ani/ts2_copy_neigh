# PYTHON VERSION: 3.11.9

import os.path
import tkinter as tk
from tkinter.messagebox import askyesno
import webbrowser
import json

import ts2_backend as ts2
import utils.utiles as util

class App:

    logger = ""

    path_dict = os.path.join("language", "lang_dict.json")
    with open(path_dict, "r", encoding="utf-8") as file:
            lang_dict = json.load(file)

    lang_dict_en = lang_dict["lang_dict_en"]
    lang_dict_es = lang_dict["lang_dict_es"]

    def __init__(self):
        self.PY_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

        self.origin_directory = None
        self.dest_directory = None

        self.selected_language = self.lang_dict_en

        self.main_window = tk.Tk()
        self.main_window.geometry("800x600")
        self.main_window.title(self.selected_language["title"])
        self.main_window.configure(bg="#1a242b")
        self.main_window.resizable(False, False)

        self.origin_main_window = util.get_button(self.main_window, self.selected_language["origin_path"], "green", self.origin_path_button)
        self.origin_main_window.place(x=640, y=35)

        self.dest_main_window = util.get_button(self.main_window, self.selected_language["destination_path"], "green", self.dest_path_button)
        self.dest_main_window.place(x=640, y=80)

        self.execute_main_window = util.get_button(self.main_window, self.selected_language["run"], "red", self.execute_button)
        self.execute_main_window.config(state=tk.DISABLED)
        self.execute_main_window.place(x=640, y=125)

        self.language_main_window = util.get_button(self.main_window, self.selected_language["language"], "grey", self.change_language)
        self.language_main_window.place(x=640, y=455)

        self.help_main_window = util.get_button(self.main_window, self.selected_language["help"], "grey", self.help_button)
        self.help_main_window.place(x=640, y=500)

        self.label_border = tk.Frame(self.main_window, bg="#f0f0f0", relief="sunken", bd=2)
        self.label_text = tk.Label(self.label_border, font=("Consolas", 10), justify="left", anchor="nw", width=85, height=35, bg="#131313", fg="#f0f0f0")
        self.label_text.pack(fill="both", expand=True, padx=1, pady=1)
        self.label_border.pack(anchor="nw", padx=15, pady=15)
        self.output()
  
    def origin_path_button(self):
        parent_directory, self.origin_directory = ts2.select_directory()
        self.switch_state()

        self.logger += self.selected_language["selected_origin_message"].format(origin_directory=self.origin_directory)+"\n"

    def dest_path_button(self):
        parent_dest_directory, self.dest_directory = ts2.select_directory()
        self.switch_state()

        self.logger += self.selected_language["selected_destination_message"].format(dest_directory=self.dest_directory)+"\n"

    def execute_button(self):
        answer_execute = askyesno(self.selected_language["run"], self.selected_language["checking_message"])

        if answer_execute:
            self.selected_language["start_copy_message"].format(dest_directory=self.dest_directory)+"\n"

            self.logger += self.selected_language["start_copy_message"]+"\n"
            list_directory = ts2.ls_directory(self.dest_directory)
            self.logger += self.selected_language["directory_list_message"].format(list_directory=list_directory)+"\n"
            directory_name = os.path.basename(self.origin_directory)
            self.logger += self.selected_language["copying_message"].format(directory_name=directory_name)+"\n"
            renamed_folder = ts2.folder_number(list_directory, directory_name)
            self.logger += self.selected_language["start_rename_message"].format(directory_name=directory_name, renamed_folder=renamed_folder)+"\n"
            ts2.copy_folder(self.origin_directory, self.dest_directory, renamed_folder, list_directory)
            neighborhood_files = ts2.ls_directory(self.dest_directory)
            full_path = ts2.create_paths(self.dest_directory, renamed_folder)
            self.logger += self.selected_language["renaming_message"]+"\n"
            ts2.rename_files(full_path, renamed_folder)
            self.logger += self.selected_language["finished_message"]+"\n"
        else:
            pass

    def switch_state(self):
        if self.origin_directory == None or self.dest_directory == None:
            self.execute_main_window.config(state=tk.DISABLED)
        else:
            self.execute_main_window.config(state=tk.NORMAL)

    def output(self):
        self.label_text.config(text=self.logger)
        self.main_window.after(1000, self.output)

    def change_language(self):
        if self.selected_language == self.lang_dict_es:
            self.selected_language = self.lang_dict_en
            print("De español a inglés")
        else:
            self.selected_language = self.lang_dict_es
            print("De inglés a español")

        self.main_window.title(self.selected_language["title"])
        self.origin_main_window.config(text=self.selected_language["origin_path"])
        self.dest_main_window.config(text=self.selected_language["destination_path"])
        self.execute_main_window.config(text=self.selected_language["run"])
        self.language_main_window.config(text=self.selected_language["language"])
        self.help_main_window.config(text=self.selected_language["help"])

    def help_button(self):
        help_file_es = os.path.join("help", "ayuda.html")
        help_file_en = os.path.join("help", "help.html")

        url = {
            "es": os.path.join(self.PY_FILE_PATH, help_file_es),
            "en": os.path.join(self.PY_FILE_PATH, help_file_en)
        }

        if self.selected_language == self.lang_dict_es:
            webbrowser.open("file://" + url["es"])
        else:
            webbrowser.open("file://" + url["en"])
            

    def exit_button(self):
        answer_exit = askyesno(self.selected_language["exit"], self.selected_language["checking_message"])

        if answer_exit:
            self.main_window.destroy()
        else:
            pass

    def start(self):
        self.main_window.protocol("WM_DELETE_WINDOW", self.exit_button)
        self.main_window.mainloop()

