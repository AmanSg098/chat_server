# server.py
import socket
import threading

import constants

clients: list[socket.socket] = []

def broadcast(message: bytes, sender: socket.socket) -> None:
    for client in clients:
        if client != sender:
            client.send(message)


def handle_client(cl_socket: socket.socket, cl_addr: tuple[str, int]) -> None:
    try:
        while True:
            received_message: str = cl_socket.recv(constants.BYTES).decode("utf-8")

            if received_message == "exit" or not received_message:
                break

            print(f"{cl_addr}: {received_message}")
            
            formatted_message: str = f"{cl_addr}: {received_message}"
            broadcast(
                formatted_message.encode("utf-8"),
                cl_socket
            )

    except (ConnectionResetError, OSError):
        pass

    finally:
        if cl_socket in clients:
            clients.remove(cl_socket)

        cl_socket.close()
        print(f"Connection from {cl_addr} closed")


server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((constants.HOST,constants.PORT))
server.listen(5)

try:
    while True:
        client_socket, client_addr = server.accept()

        clients.append(client_socket)
        print(f"Connection from {client_addr}")

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



