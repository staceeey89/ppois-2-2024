from tkinter import Button
from view import create_root
from model import show_train_data, write_in_file, Search_Info, delete_data, show_train_data_table, show_train_data_tree

def main():
    root = create_root()

    btn_show_data_table = Button(root, text='Просмотреть данные (таблица)', command=lambda: show_train_data_table(root))
    btn_show_data_table.pack()

    btn_show_data_tree = Button(root, text='Просмотреть данные (дерево)', command=lambda: show_train_data_tree(root))
    btn_show_data_tree.pack()

    btn_show_data = Button(root, text='Просмотреть данные', command=lambda: show_train_data(root))
    btn_show_data.pack()

    btn_write_file = Button(root, text='Записать в файл', command=lambda: write_in_file(root))
    btn_write_file.pack()

    btn_search_info = Button(root, text='Найти информацию', command=lambda: Search_Info(root))
    btn_search_info.pack()

    btn_delete_data = Button(root, text='Удалить данные', command=lambda: delete_data(root))
    btn_delete_data.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
