# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 08:36:37 2025

@author: zdima
"""
import tkinter as tk
from tkinter import *
import os
from datetime import datetime
import time
import sys
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
        self.current_dir =''
        
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
        self.start_vfs()
        if self.start_scr and os.path.exists(self.start_scr):
            self.start_script_run()
        elif self.start_scr:
            self.text_out(f"error: startup script not found: {self.start_scr}")    
    def start_vfs(self):
        try:
            self.zip_vfs = ZipFile(self.vfs, 'r')
            self.vfs_root = Path(self.zip_vfs)
            for item in self.zip_vfs.infolist():
                print(f"File Name: {item.filename} Date: {item.date_time} Size: {item.file_size}")
        except Exception:
            self.zip_vfs = None
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
            self.ls_com()
        elif comm == "cd":
            self.cd_com(arg)
        elif comm == "exit":
           self.exit_com()
        elif comm == "who":
            self.who_com()
        elif comm == "date":
            self.date_com()
        else:
            self.text_out("command not found: " + comm)
    def exit_com(self):
        self.root.destroy()
    def ls_com(self):
        if self.zip_vfs == None:
            self.text_out("VFS NOT FOUND")
            return
        files = [f for f in self.zip_vfs.namelist() if f[:len(self.current_dir)] == self.current_dir]
        current_dir_files = set()

        for f in files:
            relative_path = f.replace(self.current_dir, '', 1).lstrip('/')
            if '/' not in relative_path:
                current_dir_files.add(relative_path)
            else:
                dir_name = relative_path.split('/')[0]
                current_dir_files.add(dir_name)
        if self.current_dir == "":
            self.text_out("\n".join(sorted(current_dir_files)))
        else:
            current_dir_files.remove("")
            self.text_out("\n".join(sorted(current_dir_files)))
    def cd_com(self, args):
        s = args[0]
        if self.zip_vfs == None:
            self.text_out("VFS NOT FOUND")
            return
    
        if s == '..':
            if self.current_dir:
                self.current_dir = os.path.normpath(os.path.join(self.current_dir, '..'))
                if self.current_dir == '.':
                    self.current_dir = ''
            self.text_out(f"Changed directory to {self.current_dir}")
        else:
            new_path = os.path.join(self.current_dir, s)
            if not new_path[-1] == '/':
                new_path += '/'
            if any((name[:len(new_path)] == new_path) for name in self.zip_vfs.namelist()):
                self.current_dir = new_path
                self.text_out(f"Changed directory to {self.current_dir}")
                return
            else:
                self.text_out(f"cd: {args}: No such file or directory")
                return    
    def who_com(self):
        username = os.getlogin()
        self.text_out(f"Username: {username}")
    def date_com(self):
        now = datetime.now()
        # Форматируем в стиле Linux date: "Wed Sep 10 12:34:56 EEST 2025"
        formatted_date = now.strftime("%a %b %d %H:%M:%S %Z %Y")
        self.text_out(formatted_date)
        
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
