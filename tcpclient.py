import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# Initialize global variables for the socket and nickname
client = None
nickname = None

# Function to start the client connection
def start_client():
    global client, nickname
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        # Send the nickname as the first message to the server
        client.send(nickname.encode('ascii'))                                                  
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
    except Exception as e:
        print(f"Unable to connect to the server: {e}")

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.startswith('NICKNAME'):
                client.send(nickname.encode('ascii'))
            else:
                # Separate sender and received messages based on nickname
                if message.startswith(nickname + ":"):
                    display_message(message, align='right', sender=True)
                else:
                    display_message(message, align='left', sender=False)
        except Exception as e:
            print(f"Error receiving message: {e}")
            client.close()
            break

# Function to send a message
def send_message():
    message = f'{nickname}: {message_input.get()}'
    if message_input.get():  # Check if there's a message to send
        display_message(f"You: {message_input.get()}", align='right', sender=True)  # Show own message on the right side
        client.send(message.encode('ascii'))
        message_input.delete(0, tk.END)

# Function to display a message in the chat window
def display_message(message, align, sender):
    message_display.config(state=tk.NORMAL)
    
    # Configure message alignment and color
    tag_name = 'right' if align == 'right' else 'left'
    color = "#1E1E1E" if sender else "#2E8B57"  # Dark gray for self, dark green for others
    
    message_display.insert(tk.END, message + '\n', tag_name)
    message_display.tag_configure(tag_name, justify=align, foreground=color)
    
    message_display.see(tk.END)
    message_display.config(state=tk.DISABLED)

# Function to clear chat history
def clear_chat():
    message_display.config(state=tk.NORMAL)
    message_display.delete(1.0, tk.END)
    message_display.config(state=tk.DISABLED)

# Setup the GUI
def setup_gui():
    global message_display, message_input
    window = tk.Tk()
    window.title(f"Chat Client - {nickname}")
    window.geometry("400x500")

    # Display area for messages with scroll and formatting
    message_display = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD)
    message_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Input field for typing messages
    message_input = tk.Entry(window)
    message_input.pack(padx=10, pady=5, fill=tk.X)
    message_input.bind("<Return>", lambda event: send_message())  # Send on Enter key

    # Send button
    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Clear chat button
    clear_button = tk.Button(window, text="Clear Chat", command=clear_chat)
    clear_button.pack(padx=10, pady=5, side=tk.RIGHT)

    return window

# Prompt for server IP and nickname using Tkinter dialog
def prompt_for_details():
    global server_ip, nickname
    server_ip = simpledialog.askstring("Server IP", "Enter the server IP address:", initialvalue='127.0.0.1')
    nickname = simpledialog.askstring("Nickname", "Choose your nickname:")

# Main function
if __name__ == "__main__":
    # Set up Tkinter root for dialogs
    root = tk.Tk()
    root.withdraw()  # Hide the root window for now

    prompt_for_details()

    port = 5000  # Define the port here

    # Set up GUI and start client
    window = setup_gui()
    start_client()
    window.mainloop()

