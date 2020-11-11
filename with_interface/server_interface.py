from tkinter import *
import socket
import threading
import random
import time
from string import ascii_letters
from tkinter import messagebox

# SETTINGS_SERVER
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
try:
    server.bind(
        ("127.0.0.1", 1233)
    )
    server.listen(5)
except OSError:
    messagebox.showinfo("Error", "Ошибка соединения")
    raise SystemExit


users = []
statistic = ""
max_num = 2


def send_all(data):
    for user in users:
        user.send(data)


def random_char(user):
    global statistic
    while True:
        rand = random.randint(1, max_num)
        rand2 = random.randint(0, 5)
        data = (''.join(random.choice(ascii_letters) for _ in range(rand)))
        info2["text"] = data
        statistic = statistic + data
        data2 = data.encode("utf-8")
        time.sleep(rand2)
        send_all(data=data2)


def listen_user(user):
    global statistic
    while True:
        data = user.recv(2048)
        if data.decode('utf-8') == "stat":
            send_all(str((len(statistic))).encode('utf-8'))
            statistic = ""


def start_server():
    while True:
        user_socket, address = server.accept()
        info['text'] = f'User <{address[0]}> connected!'
        users.append(user_socket)
        listen_accepted_user = threading.Thread(target=listen_user, args=(user_socket,))
        random_accepted = threading.Thread(target=random_char, args=(user_socket,))
        random_accepted.start()
        listen_accepted_user.start()


def setup():
    global max_num
    max_num = message.get()
    if max_num.isdigit():
        max_num = int(max_num)
        thread1 = threading.Thread(target=start_server)
        thread1.start()
        btn.destroy()
        message_entry.destroy()
        frame_top.destroy()
        l1.destroy()
        frame_bottom.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.1)
        frame_bottom2.place(relx=0.15, rely=0.5, relwidth=0.7, relheight=0.1)
        messagebox.showinfo("Сервер запущен", "Сервер запущен")
    else:
        messagebox.showinfo("Введите число!", message.get())


# TKINTER_SETTINGS
root = Tk()
root['bg'] = '#fafafa'
root.title('Server')
root.geometry('300x250')
root.resizable(width=False, height=False)
frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.25)
frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.1)
frame_bottom2 = Frame(root, bg='#ffb700', bd=5)
frame_bottom2.place(relx=0.15, rely=0.75, relwidth=0.7, relheight=0.1)
message = StringVar()
l1 = Label(frame_top, text="Макс. число символов", font="Arial 9")
l1.pack()
message_entry = Entry(textvariable=message)
message_entry.place(relx=.5, rely=.1, anchor="c")
btn = Button(frame_top, text='Старт', command=setup)
btn.pack()
info = Label(frame_bottom, text='Инф-я о подключении', bg='#ffb700', font=40)
info.pack()
info2 = Label(frame_bottom2, text='Отправленные сообщения', bg='#ffb700', font=40)
info2.pack()


if __name__ == "__main__":
    root.mainloop()