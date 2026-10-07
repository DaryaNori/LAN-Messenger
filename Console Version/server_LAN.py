import socket  
import threading
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "server_log.txt")

HOST = "0.0.0.0"
PORT = 5000

clients = {}
groups = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("=" * 40)
print("LAN Messenger Server Started")
print(f"Listening on Port {PORT}")
print("=" * 40)

def write_log(text):
    print(os.path.abspath("server_log.txt"))
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{time}] {text}\n")

def broadcast(message, sender_socket):
    for username , client_socket in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                pass
# privte message for 2 person
def private_message(sender, receiver, message):
    if receiver in clients:
        receiver_socket = clients[receiver]
        receiver_socket.send(f"[PRIVATE] {sender}: {message}".encode())
        write_log(f"[PRIVATE] {sender} -> {receiver}: {message}")
    else:
        sender_socket = clients[sender]
        sender_socket.send(f"User '{receiver}' not found.".encode())

def show_users(client_socket):
    users = ",".join(clients.keys())
    client_socket.send(f"/userslist {users}".encode())

def create_group(client_socket, group_name):
    if group_name in groups:
        client_socket.send(f"Group '{group_name}' already exists.".encode())
    else:
        groups[group_name] = []
        client_socket.send(f"Group '{group_name}' created successfully.".encode())

def join_group(client_socket, username, group_name):
    if group_name not in groups:
        client_socket.send(f"Group '{group_name}' does not exist.".encode())
        return
    if username in groups[group_name]:
        client_socket.send(f"You are already a member of '{group_name}'.".encode())
        return
    groups[group_name].append(username)
    client_socket.send(f"You joined group '{group_name}' successfully.".encode())

def group_message(sender, group_name, message):
    if group_name not in groups:
        clients[sender].send(f"Group '{group_name}' does not exist.".encode())
        return
    if sender not in groups[group_name]:
        clients[sender].send(f"You are not a member of '{group_name}'.".encode())
        return
    for member in groups[group_name]:
        if member != sender and member in clients:
            clients[member].send(f"[GROUP:{group_name}] {sender}: {message}".encode())

def send_file(sender, receiver, filename):
    if receiver not in clients:
        clients[sender].send(f"User '{receiver}' not found.".encode())
        return
    if not os.path.exists(filename):
        clients[sender].send("File not found.".encode())
        return
    filesize = os.path.getsize(filename)
    clients[receiver].send(f"/receivefile {sender} {os.path.basename(filename)} {filesize}".encode())

    with open(filename, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            clients[receiver].send(data)
    clients[sender].send("File sent successfully.".encode())
    write_log(f"{sender} sent file '{filename}' to {receiver}")

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        clients[username] = client_socket
        time = datetime.now().strftime("%H:%M:%S")
        print(f"[{time}] {username} joined the server.")
        write_log(f"{username} joined the server.")
        print(f"Online Users: {len(clients)}")
        broadcast(f"{username} joined the chat.", client_socket)

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("/msg"):
                parts = message.split(" ", 2)
                if len(parts) == 3:
                    target = parts[1]
                    private_text = parts[2]
                    private_message(username, target, private_text)
                else:
                    client_socket.send("Correct format: /msg username message".encode())
                continue

            if message == "/users":
                show_users(client_socket)
                continue

            if message.startswith("/create_group"):
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    group_name = parts[1]
                    create_group(client_socket, group_name)
                else:
                    client_socket.send("Correct format: /create_group GroupName".encode())
                continue

            if message.startswith("/join"):
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    group_name = parts[1]
                    join_group(client_socket, username, group_name)
                else:
                    client_socket.send("Correct format: /join GroupName".encode())
                continue

            if message.startswith("/group"):
                parts = message.split(" ", 2)
                if len(parts) == 3:
                    group_name = parts[1]
                    group_text = parts[2]
                    group_message(
                        username,
                        group_name,
                        group_text
                    )
                else:
                    client_socket.send("Correct format: /group GroupName Message".encode())
                continue

            if message.startswith("/sendfile"):
                parts = message.split(" ", 2)
                if len(parts) == 3:
                    receiver = parts[1]
                    filename = parts[2]
                    send_file(
                        username,
                        receiver,
                        filename
                    )
                else:
                    client_socket.send("Correct format: /sendfile username filename".encode())
                continue
            
            time = datetime.now().strftime("%H:%M:%S")
            print(f"[{time}] {username}: {message}")
            write_log(f"{username}: {message}")
            broadcast(f"[{time}] {username}: {message}", client_socket)
            
    except Exception as e:
        print("Error:", e)

    finally:
        for name, sock in list(clients.items()):
            if sock == client_socket:
                del clients[name]
                time = datetime.now().strftime("%H:%M:%S")
                broadcast(f"{name} left the chat.", client_socket)
                print(f"[{time}] {name} disconnected.")
                write_log(f"{name} disconnected.")
                print(f"Online Users: {len(clients)}")
                break
        client_socket.close()

while True:
    client_socket, client_address = server.accept()
    print(f"New Connection: {client_address}")
    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )
    thread.start()