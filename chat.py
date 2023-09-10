import socket
import threading

HOST = 'localhost'  # Use localhost when running server and client on the same machine
PORT = 12345

clients = []

def handle_client(client_socket, username):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = data.decode()
        print(f"{username}: {received_message}")

def main():
    username = input("Enter your username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    clients.append(client_socket)

    # Start a thread to handle incoming messages from the server
    receive_thread = threading.Thread(target=handle_client, args=(client_socket, username))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            break
        client_socket.send(f"{username}: {message}".encode())

    clients.remove(client_socket)
    client_socket.close()

if __name__ == "__main__":
    main()
