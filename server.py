import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345  # Choose a port number

# List to store connected clients
clients = []

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Function to broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        # Send the message to all clients except the sender
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if there is an issue with sending the message
                clients.remove(client)

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Remove the client if it disconnects
                clients.remove(client_socket)
                break
            else:
                # Broadcast the message to all connected clients
                broadcast(message, client_socket)
        except:
            # Remove the client if there is an error
            clients.remove(client_socket)
            break

# Main server loop
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Connected: {client_address}")
    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
