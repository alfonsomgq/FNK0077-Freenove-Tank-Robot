import socket
from Command import COMMAND as cmd
from threading import Thread
from Thread import * #Archivo .py


class EnlaceTCP:
    def __init__(self):
        self.client_socket = None
        self.client_socket1 = None
        self.connect_Flag = False  # Esta debería ser una propiedad de esta clase

    def start_tcp_client(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        self.connect_Flag = True  # Actualiza el estado de la conexión

    def stop_tcp_client(self):
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except Exception as e:
                print(f"Error closing TCP client: {e}")


class control():
    def __init__(self, host="192.168.0.93", port=5003):
        self.TCP = EnlaceTCP()
        self.host = host
        self.port = port

    def connect(self):
        if not self.TCP.connect_Flag:
            self.TCP.start_tcp_client(self.host, self.port)
            print(f'Connected to server at {self.host}')
        else:
            self.TCP.stop_tcp_client()
            print('Disconnected from server')

    def send_data(self, data):
        if self.TCP.connect_Flag:
            try:
                # Añade automáticamente un '\n' al final del mensaje
                full_message = data.strip() + '\n'
                self.TCP.client_socket.send(full_message.encode('utf-8'))
                print(f"Sent data: {full_message}")
            except Exception as e:
                print(f"Error sending data: {e}")

    def receive_messages(self):
        if not self.TCP.connect_Flag:
            return
        try:
            while True:
                data = self.TCP.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received: {data}")
        except Exception as e:
            print(f"Error receiving data: {e}")


if __name__ == "__main__":
    control_instance = control()
    control_instance.connect()

    try:
        while True:
            command = input("Enter command (or type 'exit' to quit): ")
            if command.lower() == 'exit':
                break
            control_instance.send_data(command)
    finally:
        control_instance.connect()  # This will disconnect if connected