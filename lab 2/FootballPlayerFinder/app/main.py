import tkinter as tk

from app.controller import Controller

if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()
