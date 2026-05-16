# client.py
import socket
import threading

import constants

def receive_messages(
    cl_socket: socket.socket
) -> None:
    try:
        while True:
            message: str = cl_socket.recv(constants.BYTES).decode("utf-8")

            if not message:
                break

            print(message)

    except (ConnectionResetError, OSError):
        pass



client: socket.socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(
    (constants.HOST, constants.PORT)
)


thread: threading.Thread = threading.Thread(
    target=receive_messages,
    args=(client,),
    daemon=True
)

thread.start()

try:
    while True:
        message: str = input()

        client.sendall(
            message.encode("utf-8")
        )

        if message == "exit":
            break

except KeyboardInterrupt:
    pass
finally:
    client.close()



