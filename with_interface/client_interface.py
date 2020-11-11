from tkinter import *
import threading
import socket
from threading import Thread
from tkinter import messagebox

# SETTINGS_CLIENT
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

try:
    client.connect(
        ("127.0.0.1", 1233)
    )
except ConnectionRefusedError:
    messagebox.showinfo("Error", "Ошибка соединения")
    raise SystemExit


def listen_server():
    try:
        client.recv(2048)
    except ConnectionResetError:
        messagebox.showinfo("Error", "Ошибка соединения")
        root.destroy()
        raise SystemExit
    btn = Button(frame_top, text='Посмотреть статистику', command=statistic)
    btn.pack()
    while True:
        data = client.recv(2048)
        if data.decode("utf-8").isdigit():
            int(data.decode("utf-8"))
            info2['text'] = str(data.decode("utf-8"))
        else:
            info['text'] = str(data.decode("utf-8"))


def send_server():

    listen_thread = Thread(target=listen_server)
    listen_thread.start()
    while True:
        client.send(input().encode("utf-8"))


def statistic():
    client.send("stat".encode('utf-8'))


# SETTINGS_TKINTER
root = Tk()
root['bg'] = '#fafafa'
root.title('Client')
root.geometry('300x250')
root.resizable(width=False, height=False)
frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.25)
frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.1)
frame_bottom2 = Frame(root, bg='#ffb700', bd=5)
frame_bottom2.place(relx=0.15, rely=0.75, relwidth=0.7, relheight=0.1)
info = Label(frame_bottom, text='Сообщения от сервера', bg='#ffb700', font=40)
info.pack()
info2 = Label(frame_bottom2, text='Статистика', bg='#ffb700', font=40)
info2.pack()

if __name__ == "__main__":
    thread1 = threading.Thread(target=send_server)
    thread1.start()
    root.mainloop()
