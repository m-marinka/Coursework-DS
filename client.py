import socket
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox
import random
import pickle
import numpy as np
import tqdm
import os


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

    def generate_file(self, file_name):
        numbers = [np.random.randint(0, 1000000000) for _ in range(1000001)]
        new_file = open(file_name, 'a')
        new_file.write(str(numbers).replace(", ", " "))

    def send_file(self, new_file):
        self.client_socket.send(('file_name:' + new_file).encode('utf-8'))

    def on_generate_button(self):
        file_name = self.filename_widget.get()
        if len(file_name) == 0:
            messagebox.showerror(
                "Enter a filename to generate a file")
            return
        else:
            self.filename_widget.config(state='disabled')
            self.generate_file(file_name)
            self.send_file(file_name)
            # self.client_socket.send(f"{file_name}{2048}".encode('utf-8'))

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)


if __name__ == '__main__':
    root = Tk()
    gui = Client(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
