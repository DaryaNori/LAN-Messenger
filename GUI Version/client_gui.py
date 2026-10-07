import tkinter as tk #برای بخش گرافیکی برنامه
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import simpledialog
import socket
import threading
from tkinter import filedialog

HOST = "127.0.0.1"
PORT = 5000
client = None

window = tk.Tk()
window.title("BON MOT")
window.geometry("800x400")
window.minsize(600, 400)
window.configure(bg="#E295C6")

title = tk.Label( 
    window,
    text="BON MOT Messenger",
    font=("Agency FB", 28, "bold"),
    bg="#D0006F",
    fg="white"
    )
title.pack(pady=20)

connection_frame = tk.Frame(
    window,
    bg="#D0006F"
    )
connection_frame.pack(pady=10)

main_frame = tk.Frame(
    window,
    bg="#E295C6"
)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

users_frame = tk.Frame(
    main_frame,
    bg="#D0006F",
    width=180
)

users_frame.pack(
    side="left",
    fill="y",
    padx=5
)

users_title = tk.Label(
    users_frame,
    text="Online Users",
    font=("Agency FB", 18, "bold"),
    bg="#D0006F",
    fg="white"
)
users_title.pack(pady=10)

users_list = tk.Listbox(
    users_frame,
    width=20,
    height=20,
    font=("Segoe UI", 11)
)

users_list.pack(
    padx=10,
    pady=5,
    fill="y"
)

username_label = tk.Label(
    connection_frame,
    text="Username:",
    font=("B Nazanin", 8),
    bg="#131313",
    fg="white"
    )
username_label.grid(row=0, column=0, padx=5, pady=5)

username_entry = tk.Entry(
    connection_frame,
    width=25,
    font=("Agency FB", 12)
    )
username_entry.grid(row=0, column=1, padx=5, pady=5)

chat_box = scrolledtext.ScrolledText(
    main_frame,
    width=70,
    height=20,
    font=("Segoe UI", 11),
    bg="white",
    fg="black"
)
chat_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)
chat_box.see(tk.END)
chat_box.config(state="disabled")

message_frame = tk.Frame(
    window,
    bg="#E295C6"
)
message_frame.pack(pady=10)

message_label = tk.Label(
    message_frame,
    text="Message:",
    font=("Agency FB", 14),
    bg="#E295C6",
    fg="black"
)
message_label.grid(row=0, column=0, padx=5)

message_entry = tk.Entry(
    message_frame,
    width=45,
    font=("Segoe UI", 12)
)
message_entry.grid(row=0, column=1, padx=10)
message_entry.focus()

def connect_server():
    global client
    username = username_entry.get().strip()
    if username == "":
        messagebox.showerror(
            "Error",
            "Please enter a username."
        )
        return 
    try:
        client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(username.encode())
        thread = threading.Thread(target=receive_messages)
        thread.daemon = True
        thread.start()
        messagebox.showinfo( "Success", "Connected to server.")
        connect_button.config(state="disabled")
        username_entry.config(state="disabled")
    except Exception as e:
        messagebox.showerror(
            "Connection Error",
            str(e)
        )
connect_button = tk.Button(
    connection_frame,
    text="Connect",
    bg="#D0006F",
    fg="white",
    command=connect_server
)
connect_button.grid(row=0, column=2, padx=5, pady=5)

def show_online_users():
    global client
    if client is None:
        messagebox.showerror(
            "Error",
            "Please connect to the server first."
        )
        return
    client.send("/users".encode())
users_button = tk.Button(
    connection_frame,
    text="Online Users",
    bg="#E295C6",
    fg="white",
    command=show_online_users
)
users_button.grid(row=0, column=3, padx=5, pady=5)

def create_group():
    global client
    if client is None:
        messagebox.showerror(
            "Error",
            "Please connect first."
        )
        return
    group_name = simpledialog.askstring(
        "Create Group",
        "Enter group name:"
    )
    if not group_name:
        return
    try:
        client.send(f"/create_group {group_name}".encode())
    except:
        messagebox.showerror(
            "Error",
            "Connection lost."
        )
group_button = tk.Button(
    connection_frame,
    text="Create Group",
    bg="#D0006F",
    fg="white",
    command=create_group
)
group_button.grid(
    row=0,
    column=4,
    padx=5,
    pady=5
)

def update_users_list(users):
    users_list.delete(0, tk.END)
    for user in users.split(","):
        users_list.insert( tk.END, user)

def select_user(event):
    selection = users_list.curselection()
    if not selection:
        return
    username = users_list.get(selection[0])
    message_entry.delete(0, tk.END)
    message_entry.insert(
        0,
        f"/msg {username} "
    )
    message_entry.focus()
users_list.bind("<Double-Button-1>", select_user)

def receive_messages():
    global client
    while True:
        try:
            message = client.recv(1024).decode()
            if message.startswith("/userslist"):
                users = message.replace( "/userslist ", "")
                update_users_list(users)
                continue
            if not message:
                break
            chat_box.config(state="normal")
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state="disabled")
            chat_box.see(tk.END)
        except:
            chat_box.config(state="normal")
            chat_box.insert(tk.END, "\nDisconnected from server.\n")
            chat_box.config(state="disabled")
            chat_box.see(tk.END)
            break

def send_file():
    global client
    if client is None:
        messagebox.showerror(
            "Error",
            "Please connect to the server first."
        )
        return
    receiver = simpledialog.askstring(
        "Receiver",
        "Enter receiver username:"
    )
    if not receiver:
        return
    filename = filedialog.askopenfilename()
    if not filename:
        return
    try:
        client.send(f"/sendfile {receiver} {filename}".encode())
        messagebox.showinfo(
            "Success",
            "File is being sent."
        )
    except:
        messagebox.showerror(
            "Error",
            "Could not send file."
        )

def join_group():
    global client
    if client is None:
        messagebox.showerror(
            "Error",
            "Please connect first."
        )
        return
    group_name = simpledialog.askstring(
        "Join Group",
        "Enter group name:"
    )
    if not group_name:
        return
    try:
        client.send(f"/join {group_name}".encode())
        messagebox.showinfo(
            "Success",
            f"Join request sent for '{group_name}'."
        )
    except:
        messagebox.showerror(
            "Error",
            "Connection lost."
        )
join_button = tk.Button(
    connection_frame,
    text="Join Group",
    bg="#D0006F",
    fg="white",
    command=join_group
)
join_button.grid(
    row=0,
    column=5,
    padx=5,
    pady=5
)

def send_message():
    global client
    if client is None:
        messagebox.showerror("Error", "Please connect to the server first.")
        return
    message = message_entry.get().strip()

    if message == "":
        return
    try:
        client.send(message.encode())
        chat_box.config(state="normal")
        chat_box.insert(tk.END, "You: " + message + "\n")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)
        message_entry.delete(0, tk.END)
    except:
        messagebox.showerror(
            "Error",
            "Connection lost."
        )
message_entry.bind("<Return>", lambda event: send_message())
file_button = tk.Button(
    message_frame,
    text="File",
    width=10,
    bg="#D0006F",
    fg="white",
    font=("Agency FB", 13, "bold"),
    command=send_file
)
file_button.grid(
    row=0,
    column=3,
    padx=10
)
send_button = tk.Button(
    message_frame,
    text="Send",
    width=10,
    bg="#D0006F",
    fg="white",
    font=("Agency FB", 13, "bold"),
    command=send_message
)
send_button.grid(row=0, column=2, padx=10)

def close_window():
    global client
    try:
        if client is not None:
            client.close()
    except:
        pass
    window.destroy()
window.protocol("WM_DELETE_WINDOW", close_window)
window.mainloop()
