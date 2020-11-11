import socket
import threading
import random
import time
from string import ascii_letters

# SERVER_SETTINGS
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

try:
    server.bind(
        ("127.0.0.1", 1233)
    )
    server.listen(5)
    print('Server is listening')
except OSError:
    print('Уже установлено соединение по этому адресу')


users = []
statistic = ""


def send_all(data):
    for user in users:
        user.send(data)


def random_char():
    global statistic
    while True:
        rand_char_value = random.randint(0, 20)
        rand_time_value = random.randint(0, 5)
        data = (''.join(random.choice(ascii_letters) for _ in range(rand_char_value)))
        statistic = statistic + data
        data_2_send = data.encode("utf-8")
        time.sleep(rand_time_value)
        send_all(data=data_2_send)


def listen_user(user):
    global statistic
    print("Listening user")
    while True:
        data = user.recv(2048)
        if data.decode('utf-8') == "stat":
            send_all(str((len(statistic))).encode('utf-8'))
            statistic = ""


def start_server():
    while True:
        user_socket, address = server.accept()
        print(f'User <{address[0]}> connected!')
        users.append(user_socket)
        listen_accepted_user = threading.Thread(target=listen_user, args=(user_socket,))
        random_accepted = threading.Thread(target=random_char(), args=(user_socket,))
        random_accepted.start()
        listen_accepted_user.start()


if __name__ == '__main__':
    try:
        start_server()
    except OSError:
        pass
