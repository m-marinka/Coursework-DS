import socket
import threading
import numpy as np
import time


class Server:
    clients_list = []

    last_received_message = ""

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_listening_server()

    def create_listening_server(self):
        local_ip = '127.0.0.1'
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, so):
        while True:
            incoming_buffer = so.recv(256)
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            if "file_name" in self.last_received_message:
                file_name = self.last_received_message.split(":")[1]
                self.sort_file_data(file_name)
            elif "echo" in self.last_received_message:
                echo_message = self.last_received_message.split(":")[1]
                self.return_echo_message(echo_message)
            self.broadcast_to_all_clients(so)  # send to all clients
        so.close()

    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)

    def sort_file_data(self, file_name):
        open_file = open(file_name, 'r')
        file_read = open_file.read()
        read = file_read.replace('[', '').replace(']', '')
        split_list = read.split(' ')
        int_list = list(map(int, split_list))
        start_time = time.time()
        sorted_array = self.quick_sort(int_list)
        print("--- %s seconds ---" % (time.time() - start_time))
        file_write = open(file_name, 'w')
        file_write.write(str(sorted_array).replace(", ", " "))
        open_file.close()
        file_write.close()

    def quick_sort(self, array: []):
        if len(array) < 2:
            return array
        else:
            pivot = array[0]
            less = [i for i in array[1:] if i <= pivot]
            greater = [i for i in array[1:] if i > pivot]
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

    def return_echo_message(self, echo_message):
        self.server_socket.send(echo_message.encode('utf-8'))


if __name__ == "__main__":
    Server()
