import socket
import threading

def send_discovery_message(username):
    discovery_message = f"{username} has joined the chat."
    s.sendto(discovery_message.encode(), (broadcast_address, port))

def send_messages(username):
    while True:
        message = input(f"{username} ({port}): ")
        s.sendto(f"{username} ({port}): {message}".encode(), (broadcast_address, port))

def receive_messages():
    while True:
        data, _ = s.recvfrom(1024)
        print(data.decode())

port = 12345  # Use the same port number for all peers
broadcast_address = '<broadcast>'  # Broadcast address to send to all peers

# Get the username from the user
username = input("Enter your username: ")

# Create a UDP socket for broadcasting
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the port for receiving
s.bind(('0.0.0.0', port))

print(f"Listening for messages on port {port}")

# Send a discovery message when a peer joins
send_discovery_message(username)

# Create threads for sending and receiving messages
send_thread = threading.Thread(target=send_messages, args=(username,))
receive_thread = threading.Thread(target=receive_messages)

# Start the threads
send_thread.start()
receive_thread.start()
