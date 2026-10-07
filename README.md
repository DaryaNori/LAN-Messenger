💬 LAN Messenger

A local LAN messaging system built with Python socket programming.

This project was developed as a class project for a Computer Networks course. It provides a simple client-server messaging system that allows users connected to the same local network to communicate and exchange files.

✨ Features

- 💬 Send and receive text messages
- 👥 Communicate with connected clients
- 📁 Send files over the local network
- 👨‍👩‍👧‍👦 Create and manage work groups
- 🖥️ Console-based client and server
- 🎨 GUI-based client
- 📝 Server-side logging
- 🌐 LAN-based communication
- 🔌 Client-Server architecture using Python sockets

🛠️ Technologies

- Python
- Socket Programming
- TCP/IP
- LAN Networking
- Tkinter
- PyInstaller

📂 Project Structure

LAN-Messenger/
│
├── Console Version/
│   ├── client.py
│   ├── server_LAN.py
│   └── ...
│
├── GUI Version/
│   ├── client_gui.py
│   └── ...
│
├── .gitignore
└── README.md

🖥️ Project Versions

Console Version

The console version provides the core client-server communication features through the command line.

It includes:

- Client connection to the server
- Text messaging
- File transfer
- Group communication
- Server logging

🎨 GUI Version

The GUI version provides a graphical interface for interacting with the messaging system.

It makes the client easier to use by providing a visual interface for:

- Connecting to the server
- Sending and receiving messages
- Communicating with other clients
- Working with groups
- Sending files

⚙️ How to Run

1. Start the Server

First, run:

python server_LAN.py

The server should be started before connecting clients.

2. Start the Client

Then run the client:

python client.py

For the graphical version:

python client_gui.py

3. Connect Clients

Clients connected to the same LAN can communicate through the server.

🌐 Architecture

The project follows a basic Client-Server architecture:

                 ┌───────────────┐
                 │     Server    │
                 │   Python      │
                 │    Socket     │
                 └───────┬───────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
        Client 1     Client 2     Client 3

The server manages client connections and handles communication between connected users.

🚀 Future Improvements

Possible future improvements include:

- 🔐 User authentication
- 🔒 Encrypted communication
- 💾 Database integration
- 🟢 Online/offline user status
- 📱 Improved responsive interface
- 🔔 Message notifications
- 👤 User profiles
- 📊 Better server management

🎓 Academic Project

This project was developed as part of a Computer Networks course to practice concepts such as:

- Client-Server Architecture
- Socket Programming
- TCP/IP Communication
- LAN Networking
- File Transfer
- Multi-Client Communication

👩🏻‍💻 Author

Darya Nori

GitHub: "DaryaNori" (https://github.com/DaryaNori)

---

⭐ If you find this project useful, feel free to explore the code and try it on a local network.
