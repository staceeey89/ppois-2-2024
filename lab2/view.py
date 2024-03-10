from tkinter import *
from tkinter import ttk
from model import create_toolbar

def create_root():
    root = Tk()

    create_toolbar(root)

    root.title("Расписание поездов")
    root.geometry("1000x600")

    title_label = Label(root, text="Расписание поездов", font=("Helvetica", 20, "bold"))
    title_label.pack(pady=10)

    description_label = Label(root, text="Добро пожаловать! Это приложение позволяет просматривать, записывать и удалять информацию о поездах.",
                               font=("Arial", 12))
    description_label.pack(pady=10)

    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', pady=20)

    return root


