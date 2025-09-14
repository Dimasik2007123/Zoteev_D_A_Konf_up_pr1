# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 06:42:38 2025

@author: zdima
"""

import tkinter as tk
from tkinter import *
import os
import sys
import time
import platform
from zipfile import ZipFile, Path
def get_names():
    username = os.getlogin()
    hostname = platform.node()
    return username, hostname
class Emulator:
    def __init__(self, root, vfs=None, start_scr=None):
        self.root = root
        if vfs:
            self.vfs = vfs
        else:
            self.vfs = os.path.expanduser("~/.my_vfs")
        self.start_scr = start_scr
        
        #вывод параметров
        print("Параметры эмулятора")
        print("VFS - " + self.vfs)
        print("Start Script - " + self.start_scr)
        
        self.username, self.hostname = get_names()
        self.root.title("Эмулятор - " + self.username + "@" + self.hostname)
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.command_entry = tk.Entry(self.input_frame, width=80)
        self.command_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", self.read_com) # Привязка Enter к обработке
        self.prompt_label = tk.Label(self.input_frame, text="Введите команду", width = 20)
        self.prompt_label.pack()
        self.but_frame = tk.Frame(root)
        self.but_frame.pack(pady=10, padx=10, fill=tk.X)
        self.enter_but = tk.Button(self.but_frame, text = "Выполнить команду", width = 20, pady =5, command = self.read_com)
        self.enter_but.pack(side=tk.LEFT, fill = tk.BOTH)
        self.output_frame = tk.Frame(root)
        self.output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.output_text = tk.Text(self.output_frame)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        if self.start_scr and os.path.exists(self.start_scr):
            self.start_script_run()
        elif self.start_scr:
            self.text_out(f"error: startup script not found: {self.start_scr}")
        self.start_vfs()    
    def start_vfs(self):
        try:
            self.zip_vfs = ZipFile(self.vfs, 'r')
            self.vfs_root = Path(self.zip_vfs)
            for item in self.zip_vfs.infolist():
                print(f"File Name: {item.filename} Date: {item.date_time} Size: {item.file_size}")
        except Exception:
            self.text_out("VFS NOT FOUND")
    def text_out(self, s):
        self.output_text.insert(tk.END, s + "\n")
        self.output_text.see(tk.END)

    def read_com(self, event=None, text=None):
        if text is None:
            text = self.command_entry.get()
            self.command_entry.delete(0, tk.END)
        if not text:
            return
        self.text_out(self.username + "@" + self.hostname + "$ " + text)
        
        #парсер
        try:
            comm = text.split()[0]
            arg = text.split()[1:]
        except ValueError as e:
            self.text_out("error: command format " + e)
        
        if comm == "ls":
            self.ls_com(arg)
        elif comm == "cd":
            self.cd_com(arg)
        elif comm == "exit":
           self.exit_com()
        else:
            self.text_out("command not found: " + comm)
    def exit_com(self):
        self.root.destroy()
    def ls_com(self, args):
        self.text_out("Заглушка ls")
        if len(args) > 0:
            self.text_out(f"аргументы: {' '.join(args)}")
    def cd_com(self, args):
        self.text_out("Заглушка cd")
        if len(args) > 0:
            self.text_out(f"аргументы: {' '.join(args)}")
    
    def start_script_run(self):
        with open(self.start_scr, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stripped = line.strip()
                if not stripped or stripped[0] == '#':
                    continue
                try:
                    self.read_com(text = stripped)
                except Exception as e:
                    self.text_out("error in script: " + self.start_scr + " at line " + line_num + ": " + e)
                    break
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")

    args = parser.parse_args()
    
    root = tk.Tk()
    emulator = Emulator(root, vfs = args.vfs, start_scr=args.script)
    root.mainloop()