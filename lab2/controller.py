from tkinter import Button
from view import create_root
from model import show_train_data, write_in_file, Search_Info, delete_data, show_train_data_table, show_train_data_tree, create_database, load_from_db, insert_to_db, show_train_data_from_db

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

    btn_create_db = Button(root, text='Создать БД', command=create_database)
    btn_create_db.pack()

    btn_load_from_db = Button(root, text='Загрузить из БД', command=load_from_db)
    btn_load_from_db.pack()

    btn_insert_to_db = Button(root, text='Сохранить в БД', command=insert_to_db)
    btn_insert_to_db.pack()

    btn_print_db = Button(root, text='Вывести информацию из БД', command=show_train_data_from_db)
    btn_print_db.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
