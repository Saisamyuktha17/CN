import socket
import threading

# Server configuration
host = '0.0.0.0'  # Listen on all network interfaces
port = 5000

# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))
clients = {}  # Store client addresses as keys and nicknames as values

print("Server is listening...")

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender_address):
    for client_address in clients:
        if client_address != sender_address:
            server.sendto(message, client_address)

# Function to receive new client connections and handle incoming messages
def receive_connections():
    while True:
        message, client_address = server.recvfrom(1024)

        # Check if the client is new (i.e., nickname is not set)
        if client_address not in clients:
            nickname = message.decode('ascii')
            clients[client_address] = nickname

            # Send a welcome message only to the new client
            
            print(f"Nickname of the client is {nickname}")

        else:
            # Broadcast the message to all other clients
            print(f"Received message from {clients[client_address]}: {message.decode('ascii')}")
            broadcast(message, client_address)

# Start listening for new connections
receive_connections()

