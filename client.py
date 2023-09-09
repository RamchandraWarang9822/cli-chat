import socket
import threading

# Server configuration
SERVER_HOST = '185.83.214.222'  # Change to the IP or hostname of the server
SERVER_PORT = 12345  # Use the same port as the server

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
        except:
            break

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Main client loop
while True:
    message = input()
    if message == 'exit':
        client_socket.close()
        break
    else:
        # Send the message to the server
        client_socket.send(message.encode('utf-8'))
