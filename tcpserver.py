import socket
import threading

# Server configuration
host = '0.0.0.0'  # Listen on all network interfaces
port = 5000

# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)  # Allow up to 5 clients to connect
clients = {}  # Store client connections

print("Server is listening...")

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender_socket):
    for client_socket in clients.values():
        if client_socket != sender_socket:
            client_socket.send(message)

# Function to handle each client connection
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break  # Connection closed by the client
            if address not in clients:
                nickname = message.decode('ascii')
                clients[address] = client_socket
                print(f"{nickname} has joined the chat.")
                broadcast(f"{nickname} has joined the chat.".encode('ascii'), client_socket)
            else:
                print(f"Received message from {address}: {message.decode('ascii')}")
                broadcast(message, client_socket)
        except Exception as e:
            print(f"Error with client {address}: {e}")
            break

    client_socket.close()
    del clients[address]
    print(f"Connection with {address} closed.")

# Accept new connections
def accept_connections():
    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

# Start accepting connections
accept_connections()
 