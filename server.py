# server.py
import socket
import threading

import constants

clients: dict[socket.socket, str] = {}

def broadcast(message: bytes, sender: socket.socket | None = None) -> None:
    for client in clients:
        if client != sender:
            try:
                client.sendall(message)
            except OSError:
                pass


def handle_client(cl_socket: socket.socket, cl_addr: tuple[str, int]) -> None:
    try:
        while True:
            received_message: str = cl_socket.recv(constants.BYTES).decode("utf-8")

            if received_message == "exit" or not received_message:
                break

            print(f"{cl_addr}: {received_message}")
            
            formatted_message: str = f"{clients[cl_socket]}: {received_message}"
            broadcast(
                formatted_message.encode("utf-8"),
                cl_socket
            )

    except (ConnectionResetError, OSError):
        pass

    finally:
        username: str = clients.get(cl_socket, None)
        if cl_socket in clients:
            clients.pop(cl_socket, None)
        

        cl_socket.close()
        leave_message: str = f"{username} left the chat"
        print(f"{username} left the chat.")
        broadcast(leave_message.encode("utf-8"))


server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((constants.HOST,constants.PORT))
server.listen(5)

try:
    while True:
        client_socket, client_addr = server.accept()
        print(f"Connection from {client_addr}")

        client_socket.send("Input user name : ".encode("utf-8"))
        client_username: str = client_socket.recv(constants.BYTES).decode("utf-8")

        clients[client_socket] = client_username
        join_message: str = (f"{client_username} joined the chat")
        print(join_message)
        broadcast(join_message.encode("utf-8"))

        thread: threading.Thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_addr),
            daemon=True
        )

        thread.start()

except KeyboardInterrupt:
    print("\nShutting down server...")

finally:
    server.close()



