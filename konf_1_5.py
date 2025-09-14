# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 10:42:29 2025

@author: zdima
"""

import tkinter as tk
from tkinter import *
import os
from datetime import datetime
#import time
#import sys
import platform
from zipfile import ZipFile
def get_names():
    username = os.getlogin() #получение имени пользователя
    hostname = platform.node() #получение имени хоста
    return username, hostname
class Emulator:
    def __init__(self, root, vfs=None, start_scr=None):
        self.root = root
        if vfs:
            self.vfs = vfs #получаем vfs из параметра
        else:
            self.vfs = os.path.expanduser("~/.my_vfs")
        self.start_scr = start_scr #получаем стартовый скрипт из параметра
        self.current_dir ='' #текущая директория
        
        #вывод параметров
        print("Параметры эмулятора")
        print("VFS - " + self.vfs)
        print("Start Script - " + self.start_scr)
        
        self.username, self.hostname = get_names() #получаем имя пользователя и хоста
        self.root.title("Эмулятор - " + self.username + "@" + self.hostname) #указываем их в заголовке окна
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.command_entry = tk.Entry(self.input_frame, width=80) #поле для ввода команд
        self.command_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", self.read_com) # Привязка Enter к обработке
        self.prompt_label = tk.Label(self.input_frame, text="Введите команду", width = 20)
        self.prompt_label.pack()
        self.but_frame = tk.Frame(root)
        self.but_frame.pack(pady=10, padx=10, fill=tk.X)
        self.enter_but = tk.Button(self.but_frame, text = "Выполнить команду", width = 20, pady =5, command = self.read_com) #кнопка для ввода команды
        self.enter_but.pack(side=tk.LEFT, fill = tk.BOTH)
        self.output_frame = tk.Frame(root) #окно для вывода сообщений программы
        self.output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.output_text = tk.Text(self.output_frame)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.start_vfs()
        if self.start_scr and os.path.exists(self.start_scr):
            self.start_script_run() #если в системе есть стартовый скрипт, запускаем его
        elif self.start_scr:
            self.text_out(f"error: startup script not found: {self.start_scr}") #иначе выводится ошибка  
    def start_vfs(self):
        try:
            self.zip_vfs = ZipFile(self.vfs, 'r') #открываем виртуальную машину как архив
            self.vfs_files = list(self.zip_vfs.namelist()) #упорядочиваем имена всех директорий и файлов
            #self.vfs_root = Path(self.zip_vfs)
            for item in self.zip_vfs.infolist():
                print(f"File Name: {item.filename} Date: {item.date_time} Size: {item.file_size}") #в консоль выводится структура vfs для проверки
        except Exception: #если ошибка при открытии vfs
            self.zip_vfs = None
            self.vfs_files = []
            self.text_out("VFS NOT FOUND")
    def text_out(self, s):
        self.output_text.insert(tk.END, s + "\n") #функция вывода результатов на экран
        self.output_text.see(tk.END)

    def read_com(self, event=None, text=None): #функция обработки команд
        if text is None: #если не перадётся параметр извне, то получаем команду из поля ввода
            text = self.command_entry.get()
            self.command_entry.delete(0, tk.END) #очищаем поле ввода
        if not text:
            return
        self.text_out(self.username + "@" + self.hostname + "$ " + text) #дублируем команду в поле вывода
        
        #парсер
        try:
            comm = text.split()[0]
            arg = text.split()[1:]
        except ValueError as e:
            self.text_out("error: command format " + e)
        #отработка команд
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
        elif comm == "rm":
            self.rm_com(arg)
        else:
            self.text_out("command not found: " + comm)
    def exit_com(self):
        self.root.destroy() #выход из программы
    def ls_com(self):
        if self.zip_vfs == None:
            self.text_out("VFS NOT FOUND")
            return
        files = [f for f in self.vfs_files if f[:len(self.current_dir)] == self.current_dir] #получаем файлы, если они в текущей директории
        current_dir_files = set() #создаём множество

        for f in files:
            relative_path = f.replace(self.current_dir, '', 1).lstrip('/') #получаем относительный путь 
            if '/' not in relative_path:
                current_dir_files.add(relative_path) #это файл в текущей директории
            else:
                dir_name = relative_path.split('/')[0] #это поддиректория, берем только левую часть
                current_dir_files.add(dir_name)
        if self.current_dir == "":
            self.text_out("\n".join(sorted(current_dir_files))) #чтобы в выводе не было лишнего переноса строки
        else:
            current_dir_files.remove("")
            self.text_out("\n".join(sorted(current_dir_files)))
    def cd_com(self, args):
        if not args:
            self.text_out("rm: missing argument")
            return
        s = args[0]
        if self.zip_vfs == None:
            self.text_out("VFS NOT FOUND")
            return
    
        if s == '..': #переход на директорию выше
            if self.current_dir:
                self.current_dir = os.path.normpath(os.path.join(self.current_dir, '..'))#построение пути к родительской директории
                if self.current_dir == '.': #проверка на корневую директорию
                    self.current_dir = ''
            self.text_out(f"Changed directory to {self.current_dir}")
        else:
            new_path = os.path.join(self.current_dir, s)#путь, куда надо перейти
            if not new_path[-1] == '/':#приводим к общему формату
                new_path += '/'
            if any((name[:len(new_path)] == new_path) for name in self.vfs_files):#Проверяется, существует ли такая директория в списке файлов виртуальной файловой системы
                self.current_dir = new_path
                self.text_out(f"Changed directory to {self.current_dir}")
                return
            else:
                self.text_out(f"cd: {args}: No such file or directory")
                return    
    def who_com(self):
        username = os.getlogin() #получаем имя пользователя
        self.text_out(f"Username: {username}")
    def date_com(self):
        now = datetime.now() #получаем дату и время
        # Форматируем в стиле Linux date: "Wed Sep 10 12:34:56 EEST 2025"
        formatted_date = now.strftime("%a %b %d %H:%M:%S %Z %Y")
        self.text_out(formatted_date)
    def rm_com(self, args):
        if not args:
            self.text_out("rm: missing operand")
            return
        if self.zip_vfs is None:
            self.text_out("VFS NOT FOUND")
            return
        flag = 1 #метка для определения, удаляем файл или директорию
        for arg in args:
            if args[0] == "-r" and flag == 1:#если параметр -r и удаляем директорию, то переходим к следующему аргументу
                flag = 2
                continue
            if flag == 2:
                target_path = os.path.normpath(os.path.join(self.current_dir, arg)).replace(os.sep, '/')#формируется путь для удаления
                if target_path[-1] == '/':
                    dir_path = target_path
                else:
                    dir_path = target_path + '/'#приводим путь к общему формату
                is_dir = any(name[:len(dir_path)] == dir_path and name != target_path for name in self.vfs_files)#является ли путь директорией
                if is_dir:
                    self.vfs_files = [name for name in self.vfs_files if not name[:len(dir_path)] == dir_path]#Удаляются все файлы из self.vfs_files, пути которых начинаются с dir_path
                    self.text_out(f"rm: directory '{arg}' removed (in memory)")
                else:
                    if target_path in self.vfs_files:
                        self.vfs_files.remove(target_path)#если путь - не директория, то удаляем файл из памяти
                        self.text_out(f"rm: file '{arg}' removed (in memory)")
                    else:
                        self.text_out(f"rm: cannot remove '{arg}': No such file or directory")
            if flag == 1:
                target_path = os.path.normpath(os.path.join(self.current_dir, arg)).replace(os.sep, '/')#формируется путь для удаления
                if target_path[-1] == '/':
                    dir_path = target_path
                else:
                    dir_path = target_path + '/' #приводим путь к общему формату
                is_dir = any(name[:len(dir_path)] == dir_path and name != target_path for name in self.vfs_files) #является ли путь директорией
                if is_dir:
                    self.text_out("Ошибка: работа только с файлами")
                    return
                if target_path in self.vfs_files:
                    self.vfs_files.remove(target_path) #если путь - не директория, то удаляем файл из памяти
                    self.text_out(f"rm: file '{arg}' removed (in memory)")
                else:
                    self.text_out(f"rm: cannot remove '{arg}': No such file or directory")
    def start_script_run(self):
        with open(self.start_scr, 'r', encoding='utf-8') as f: #открытие стартового скрипта
            for line_num, line in enumerate(f, 1): #построчно читаем команды
                stripped = line.strip()
                if not stripped or stripped[0] == '#': #если строка пустая или содержит комментарий, то переходим к следующей
                    continue
                try:
                    self.read_com(text = stripped) #в обработчик команд отправляем прочитанную команду
                except Exception as e:
                    self.text_out("error in script: " + self.start_scr + " at line " + line_num + ": " + e)
                    break
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script") #для разделения аргументов командной строки

    args = parser.parse_args()
    
    root = tk.Tk()
    emulator = Emulator(root, vfs = args.vfs, start_scr=args.script)
    root.mainloop()