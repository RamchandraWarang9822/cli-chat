import socket
import threading

HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345

def handle_client(client_socket, username):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = data.decode()
        print(f"{username}: {received_message}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Listening on {HOST}:{PORT}")

    clients = []

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        username = client_socket.recv(1024).decode()
        print(f"{username} connected")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
        client_handler.start()

if __name__ == "__main__":
    main()
