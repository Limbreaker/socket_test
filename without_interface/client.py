import socket
from threading import Thread

# CLIENT_SETTINGS
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
try:
    client.connect(
        ("127.0.0.1", 1233)
    )
except ConnectionRefusedError:
    print('Ошибка соединения')


def listen_server():
    while True:
        try:
            data = client.recv(2048)
            print(data.decode("utf-8"))
        except OSError:
            print('Ошибка получения данных от сервера')
            break


def send_server():
    listen_thread = Thread(target=listen_server)
    listen_thread.start()

    while True:
        client.send(input().encode("utf-8"))


if __name__ == "__main__":
    send_server()
