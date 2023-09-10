import socket

HOST = 'localhost'  # Use localhost when running server and client on the same machine
PORT = 12346

def main():
    username = input("Enter your username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(username.encode())

    while True:
        message = input()
        if message.lower() == "exit":
            break
        client_socket.send(f"{username}: {message}".encode())

    client_socket.close()

if __name__ == "__main__":
    main()
