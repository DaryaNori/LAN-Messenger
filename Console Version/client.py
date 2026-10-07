import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Connected to server.")

username = input("Enter your username: ")
client.send(username.encode())

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message.startswith("/receivefile"):
                parts = message.split()
                sender = parts[1]
                filename = parts[2]
                filesize = int(parts[3])
                with open("received_" + filename, "wb") as file:
                    remaining = filesize
                    while remaining > 0:
                        data = client.recv(min(1024, remaining))
                        file.write(data)
                        remaining -= len(data)
                print(f"\nFile '{filename}' received from {sender}")
                continue
            print("\n" + message)

        except:
            print("Connection Closed.")
            client.close()
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    try:

        message = input()
        if message.strip() == "":
            continue
        client.send(message.encode())

    except Exception as e:
        print("Client Error:", e)
        client.close()
        break
