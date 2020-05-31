import socket
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox
import random
import pickle
import numpy as np


class Client:
    client_socket = None

    def __init__(self, master):
        self.root = master
        self.initialize_socket()
        self.filename_widget = None
        self.initialize_gui()
        self.on_generate_button = None

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '127.0.0.1'
        remote_port = 10319
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_filename_section()

    def display_filename_section(self):
        frame = Frame()
        Label(frame, text='Enter a filename: ', font=('Helvetica', 12)).pack(side='left', padx=10)
        self.filename_widget = Entry(frame, width=50, borderwidth=2)
        self.filename_widget.pack(side='left', anchor='sw')
        self.on_generate_button = Button(frame, text='Generate', width=10, command=self.on_generate_button).pack(
            side='left')
        frame.pack(side='bottom', anchor='e')

    def on_generate_button(self):
        if len(self.filename_widget.get()) == 0:
            messagebox.showerror(
                "Enter a filename to generate a file")
            return
        else:
            self.filename_widget.config(state='disabled')
            self.generate_file()
            self.client_socket.send()

    def generate_file(self):
        numbers = [np.random.randint(0, 1000000000) for _ in range(1000005)]
        filename = input(str())
        with open(filename, 'a') as file:
            file.write(' '.join(map(str, numbers)))

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)
