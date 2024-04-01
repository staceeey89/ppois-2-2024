import tkinter as tk

from view import View
from controller import Controller

v = View()
# c = Controller(v)

v.create_window()
v.start_window()

# root = tkinter.Tk()
# root.title("main")
# root.geometry("400x300")
#
# root.mainloop()
# root.title("dsdsd")
# frame = tkinter.Frame(root)
# frame.pack(side=tkinter.TOP, fill=tkinter.X)
# button = tkinter.Button(frame,text="btn1",command=None)
# button.pack(side=tkinter.LEFT)

# class PaginatedTextViewer:
#     def __init__(self, data, lines_per_page=10):
#         self.data = data
#         self.lines_per_page = lines_per_page
#         self.current_page = 0
#
#         self.root = tk.Tk()
#         self.root.title("Text Viewer")
#
#         self.text_widget = tk.Text(self.root, wrap="word", height=15, width=50)
#         self.text_widget.pack(side="top", fill="both", expand=True)
#
#         self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.text_widget.yview)
#         self.scrollbar.pack(side="right", fill="y")
#
#         self.text_widget.config(yscrollcommand=self.scrollbar.set)
#
#         self.update_text()
#
#         self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_page)
#         self.prev_button.pack(side="left", padx=5, pady=5)
#
#         self.next_button = tk.Button(self.root, text="Next", command=self.next_page)
#         self.next_button.pack(side="left", padx=5, pady=5)
#
#     def update_text(self):
#         start_index = self.current_page * self.lines_per_page
#         end_index = start_index + self.lines_per_page
#         page_data = self.data[start_index:end_index]
#         text = "\n".join(page_data)
#         self.text_widget.delete("1.0", "end")
#         self.text_widget.insert("1.0", text)
#
#     def next_page(self):
#         if (self.current_page + 1) * self.lines_per_page < len(self.data):
#             self.current_page += 1
#             self.update_text()
#
#     def prev_page(self):
#         if self.current_page > 0:
#             self.current_page -= 1
#             self.update_text()
#
#     def run(self):
#         self.root.mainloop()
#
# # Пример использования:
# data = [f"Line {i+1}" for i in range(100)]  # Пример данных
# viewer = PaginatedTextViewer(data)
# viewer.run()