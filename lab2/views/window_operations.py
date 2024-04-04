def window_center(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def widget_center(widget, root_width, y):
    x = (root_width - widget.winfo_reqwidth()) / 2
    widget.place(x=x, y=y)


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
