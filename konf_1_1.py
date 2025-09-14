# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 07:52:40 2025

@author: zdima
"""
import tkinter as tk
from tkinter import *
import os
import sys
import time
import platform
def get_names():
    username = os.getlogin()
    hostname = platform.node()
    return username, hostname
class Emulator:
    def __init__(self, root):
        self.root = root
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
    
    def text_out(self, s):
        self.output_text.insert(tk.END, s + "\n")
        self.output_text.see(tk.END)

    def read_com(self, event=None):
        text = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        if len(text) == 0:
            return
        self.text_out(self.username + "@" + self.hostname + "$ " + text)
        
        #парсер
        comm = text.split()[0]
        arg = text.split()[1:]
        
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
        
if __name__ == "__main__":
    root = tk.Tk()
    emulator = Emulator(root)
    root.mainloop()
