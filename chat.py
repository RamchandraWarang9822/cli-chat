import socket
import threading

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

        print(f"Server listening on {self.ip}:{self.port}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connected to {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
            self.clients.append(client_socket)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                print(f"Received from {client_socket.getpeername()}: {message}")
                # Broadcast the message to all clients except the sender
                for client in self.clients:
                    if client != client_socket:
                        client.send(message.encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

    def send_message(self, message):
        try:
            self.socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                print(f"Received: {message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def start(self):
        if self.connect_to_server():
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            while True:
                message = input()
                self.send_message(message)

if __name__ == "__main__":
    # Automatically detect the server IP on the local network
    server_ip = None
    try:
        # Use a known hostname to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        server_ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(f"Error detecting server IP: {e}")

    if server_ip:
        print(f"Detected server IP: {server_ip}")
        server = Server(server_ip, 12345)  # Replace 12345 with your desired port
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_thread.start()

        while True:
            choice = input("Enter 'c' to start a client or 'q' to quit: ")
            if choice == 'c':
                client = Client(server_ip, 12345)  # Replace 12345 with the server's port
                client.start()
            elif choice == 'q':
                break
            else:
                print("Invalid choice. Enter 'c' to start a client or 'q' to quit.")
    else:
        print("Server IP detection failed.")
