import socket
import threading

class ChatServer:
    def __init__(self):
        self.clients = {}
        self.rooms = {}
        self.lock = threading.Lock()
        self.udp_server_socket = None
        self.create_listening_server()

    def create_listening_server(self):
        udp_local_ip = '127.0.0.1'
        udp_local_port = 10320
        
        self.udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server_socket.bind((udp_local_ip, udp_local_port))

        print("Listening for incoming UDP messages...")

        udp_thread = threading.Thread(target=self.receive_udp_messages)
        udp_thread.start()

    def receive_udp_messages(self):
        while True:
            incoming_buffer, client_address = self.udp_server_socket.recvfrom(1024)
            message = incoming_buffer.decode('utf-8')
            self.handle_message(message, client_address)

    def handle_message(self, message, client_address):
        parts = message.split('|')
        command = parts[0]

        if command == "JOIN":
            room_name = parts[1]
            username = parts[2]
            self.add_client_to_room(client_address, room_name, username)
        elif command == "MSG":
            room_name = parts[1]
            chat_message = parts[2]
            self.broadcast_message_to_room(room_name, chat_message, client_address)
        elif command == "CREATE":
            room_name = parts[1]
            self.create_room(room_name)

    def create_room(self, room_name):
        with self.lock:
            if room_name not in self.rooms:
                self.rooms[room_name] = []
                print(f"Room '{room_name}' created")

    def add_client_to_room(self, client_address, room_name, username):
        with self.lock:
            if room_name in self.rooms:
                self.rooms[room_name].append(client_address)
                self.clients[client_address] = (username, room_name)
                print(f"Client '{username}' added to room '{room_name}'")

    def broadcast_message_to_room(self, room_name, message, sender_address):
        with self.lock:
            if room_name in self.rooms:
                for client in self.rooms[room_name]:
                    if client != sender_address:
                        self.udp_server_socket.sendto(message.encode('utf-8'), client)

if __name__ == "__main__":
    ChatServer()
