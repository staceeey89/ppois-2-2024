import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from anytree import Node, RenderTree

from SearchTable import SearchResultsWindow
from controller.DB import DBPlayerController
from controller.PlayerDto import PlayerDto
from controller.XML import XmlPlayerController
from model.entity.Player import Player

db_player_controller: DBPlayerController = DBPlayerController()
xml_player_controller: XmlPlayerController = XmlPlayerController("C:/Users/Daniil/PycharmProjects/ppois-2-2024/lab2"
                                                                 "/players.xml")
is_database = True
data = db_player_controller.get_all()


class SearchWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Поиск")
        self.window.grab_set()

        self.full_name_label = ttk.Label(self.window, text="Full Name:")
        self.full_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.full_name_entry = ttk.Entry(self.window)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.birth_date_label = ttk.Label(self.window, text="Birth Date (YYYY-MM-DD):")
        self.birth_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.birth_date_entry = ttk.Entry(self.window)
        self.birth_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.football_team_label = ttk.Label(self.window, text="Football Team:")
        self.football_team_label.grid(row=2, column=0, padx=5, pady=5)
        self.football_team_entry = ttk.Entry(self.window)
        self.football_team_entry.grid(row=2, column=1, padx=5, pady=5)

        self.home_city_label = ttk.Label(self.window, text="Home City:")
        self.home_city_label.grid(row=3, column=0, padx=5, pady=5)
        self.home_city_entry = ttk.Entry(self.window)
        self.home_city_entry.grid(row=3, column=1, padx=5, pady=5)

        self.team_size_label = ttk.Label(self.window, text="Team Size:")
        self.team_size_label.grid(row=4, column=0, padx=5, pady=5)
        self.team_size_entry = ttk.Entry(self.window)
        self.team_size_entry.grid(row=4, column=1, padx=5, pady=5)

        self.position_label = ttk.Label(self.window, text="Position:")
        self.position_label.grid(row=5, column=0, padx=5, pady=5)
        self.position_entry = ttk.Entry(self.window)
        self.position_entry.grid(row=5, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.window, text="Найти", command=self.search)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

    def search(self):
        full_name: str = self.full_name_entry.get()
        birth_date: str = self.birth_date_entry.get()
        football_team: str = self.football_team_entry.get()
        home_city: str = self.home_city_entry.get()
        team_size: str = self.team_size_entry.get()
        position: str = self.position_entry.get()
        if is_database is True:
            found_players = db_player_controller.get_all()
            if full_name:
                found_players = set(db_player_controller.get_by_full_name(full_name))
            if birth_date:
                try:
                    found_players = set(found_players) & set(
                        db_player_controller.get_by_birth_date(
                            datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()))
                except ValueError:
                    show_error("Ошибка: Некорректный формат даты. Используйте формат 'YYYY-MM-DD'.")
                    return
            if football_team:
                found_players = set(found_players) & set(db_player_controller.get_by_football_team(football_team))
            if home_city:
                found_players = set(found_players) & set(db_player_controller.get_by_home_city(home_city))
            if team_size:
                try:
                    found_players = set(found_players) & set(db_player_controller.get_by_team_size(int(team_size)))
                except ValueError:
                    show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
                    return
            if position:
                found_players = set(found_players) & set(db_player_controller.get_by_position(position))
        else:
            found_players = xml_player_controller.get_all_players()
            if full_name:
                found_players = set(xml_player_controller.search_by_name(full_name))
            if birth_date:
                found_players = set(found_players) & set(xml_player_controller.search_by_birth_date(birth_date))
            if football_team:
                found_players = set(found_players) & set(xml_player_controller.search_by_football_team(football_team))
            if home_city:
                found_players = set(found_players) & set(xml_player_controller.search_by_home_city(home_city))
            if team_size:
                try:
                    found_players = set(found_players) & set(xml_player_controller.search_by_team_size(int(team_size)))
                except ValueError:
                    show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
                    return
            if position:
                found_players = set(found_players) & set(xml_player_controller.search_by_position(position))
        found_players = list(found_players)
        SearchResultsWindow(self.window, found_players)


def create_player_tree(players):
    new_root = Node("Players")
    for player in players:
        player_node = Node(str(player.id), parent=new_root)
        Node(f"id: {player.id}", parent=player_node)
        Node(f"full_name: {player.full_name}", parent=player_node)
        Node(f"birth_date: {player.birth_date}", parent=player_node)
        Node(f"football_team: {player.football_team}", parent=player_node)
        Node(f"home_city: {player.home_city}", parent=player_node)
        Node(f"team_size: {player.team_size}", parent=player_node)
        Node(f"position: {player.position}", parent=player_node)
    return new_root


def display_player_tree(players):
    player_tree = create_player_tree(players)
    tree_text = ""
    for pre, _, node in RenderTree(player_tree):
        tree_text += "%s%s\n" % (pre, node.name)
    return tree_text


def show_tree_window():
    global data
    tree_text = display_player_tree(data)

    tree_window = tk.Toplevel()
    tree_window.title("Player Tree")

    tree_text_widget = tk.Text(tree_window, wrap="none")
    tree_text_widget.insert(tk.END, tree_text)
    tree_text_widget.pack(fill=tk.BOTH, expand=True)


def show_error(message):
    messagebox.showerror("Ошибка", message)


def save():
    if messagebox.askyesno("Сохранение", "Вы хотите сохранить изменения?"):
        db_player_controller.save_db()
        xml_player_controller.save()


def on_exit():
    if messagebox.askyesno("Выход", "Вы хотите выйти из приложения?"):
        root.destroy()


def validate_input(full_name, birth_date_str, football_team, home_city, team_size_str, position):
    if not full_name.strip():
        show_error("Ошибка: Поле 'full_name' не должно быть пустым.")
        return False

    try:
        datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")
    except ValueError:
        show_error("Ошибка: Некорректный формат даты. Используйте формат 'YYYY-MM-DD'.")
        return False

    if not football_team.strip():
        show_error("Ошибка: Поле 'football_team' не должно быть пустым.")
        return False
    if not home_city.strip():
        show_error("Ошибка: Поле 'home_city' не должно быть пустым.")
        return False
    if not position.strip():
        show_error("Ошибка: Поле 'position' не должно быть пустым.")
        return False

    team_size_str = team_size_str.strip()
    if not team_size_str.isdigit():
        show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
        return False

    return True


def display_players():
    global current_page, records_per_page, treeview, data

    for row in treeview.get_children():
        treeview.delete(row)

    if is_database:
        data = db_player_controller.get_all()
    else:
        data = xml_player_controller.get_all_players()

    start = (current_page - 1) * records_per_page
    end = start + records_per_page
    for player in data[start:end]:
        record = (
            player.id, player.full_name, player.birth_date, player.football_team, player.home_city, player.team_size,
            player.position)
        treeview.insert("", "end", values=record)


def calculate_total_pages():
    global records_per_page, data
    return -(-len(data) // records_per_page)


def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        display_players()
        update_page_info()


def next_page():
    global current_page
    total_pages = calculate_total_pages()
    if current_page < total_pages:
        current_page += 1
        display_players()
        update_page_info()


def first_page():
    global current_page
    current_page = 1
    display_players()
    update_page_info()


def last_page():
    global current_page
    total_pages = calculate_total_pages()
    if current_page != total_pages:
        current_page = total_pages
        display_players()
        update_page_info()


def change_records_per_page():
    global records_per_page
    try:
        new_records_per_page = int(records_per_page_entry.get())
        if new_records_per_page > 0:
            records_per_page = new_records_per_page
            display_players()
            update_page_info()
    except ValueError:
        pass


def update_page_info():
    global current_page, records_per_page, treeview
    total_pages_label.config(text="Total Pages: {}".format(calculate_total_pages()))
    current_page_label.config(text="Current Page: {}".format(current_page))
    records_per_page_label.config(text="Records per Page: {}".format(records_per_page))
    total_records_label.config(text="Total Records: {}".format(calculate_total_records()))


def calculate_total_records():
    return len(data)


def set_is_database_true():
    global is_database
    is_database = True
    first_page()


def set_is_database_false():
    global is_database
    is_database = False
    first_page()


def create_player():
    dialog = tk.Toplevel(root)
    dialog.title("Create Player")
    dialog.grab_set()

    full_name_label = ttk.Label(dialog, text="Full Name:")
    full_name_label.grid(row=0, column=0, padx=5, pady=5)
    full_name_entry = ttk.Entry(dialog)
    full_name_entry.grid(row=0, column=1, padx=5, pady=5)

    birth_date_label = ttk.Label(dialog, text="Birth Date (YYYY-MM-DD):")
    birth_date_label.grid(row=1, column=0, padx=5, pady=5)
    birth_date_entry = ttk.Entry(dialog)
    birth_date_entry.grid(row=1, column=1, padx=5, pady=5)

    football_team_label = ttk.Label(dialog, text="Football Team:")
    football_team_label.grid(row=2, column=0, padx=5, pady=5)
    football_team_entry = ttk.Entry(dialog)
    football_team_entry.grid(row=2, column=1, padx=5, pady=5)

    home_city_label = ttk.Label(dialog, text="Home City:")
    home_city_label.grid(row=3, column=0, padx=5, pady=5)
    home_city_entry = ttk.Entry(dialog)
    home_city_entry.grid(row=3, column=1, padx=5, pady=5)

    team_size_label = ttk.Label(dialog, text="Team Size:")
    team_size_label.grid(row=4, column=0, padx=5, pady=5)
    team_size_entry = ttk.Entry(dialog)
    team_size_entry.grid(row=4, column=1, padx=5, pady=5)

    position_label = ttk.Label(dialog, text="Position:")
    position_label.grid(row=5, column=0, padx=5, pady=5)
    position_entry = ttk.Entry(dialog)
    position_entry.grid(row=5, column=1, padx=5, pady=5)

    def save_player():
        full_name: str = full_name_entry.get()
        birth_date: str = birth_date_entry.get()
        football_team: str = football_team_entry.get()
        home_city: str = home_city_entry.get()
        team_size: str = team_size_entry.get()
        position: str = position_entry.get()

        if validate_input(full_name, birth_date, football_team, home_city, team_size, position):
            team_size: int = int(team_size_entry.get())
            birth_date: datetime.date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
            if is_database is True:
                new_player = PlayerDto(full_name=full_name, birth_date=birth_date, football_team=football_team,
                                       home_city=home_city, team_size=team_size, position=position, id=None)
                db_player_controller.create(new_player)
            else:
                xml_player = xml_player_controller.get_all_players()[-1]
                new_player = Player(full_name=full_name, birth_date=birth_date, football_team=football_team,
                                    home_city=home_city, team_size=team_size, position=position,
                                    id=int(xml_player.id) + 1)
                xml_player_controller.insert(new_player)
            messagebox.showinfo("Успех!", f"Игрок успешно создан!.")
            dialog.destroy()

    save_button = ttk.Button(dialog, text="Save Player", command=save_player)
    save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


def delete_players():
    dialog = tk.Toplevel(root)
    dialog.title("Delete Player")
    dialog.grab_set()

    full_name_label = ttk.Label(dialog, text="Full Name:")
    full_name_label.grid(row=0, column=0, padx=5, pady=5)
    full_name_entry = ttk.Entry(dialog)
    full_name_entry.grid(row=0, column=1, padx=5, pady=5)

    birth_date_label = ttk.Label(dialog, text="Birth Date (YYYY-MM-DD):")
    birth_date_label.grid(row=1, column=0, padx=5, pady=5)
    birth_date_entry = ttk.Entry(dialog)
    birth_date_entry.grid(row=1, column=1, padx=5, pady=5)

    football_team_label = ttk.Label(dialog, text="Football Team:")
    football_team_label.grid(row=2, column=0, padx=5, pady=5)
    football_team_entry = ttk.Entry(dialog)
    football_team_entry.grid(row=2, column=1, padx=5, pady=5)

    home_city_label = ttk.Label(dialog, text="Home City:")
    home_city_label.grid(row=3, column=0, padx=5, pady=5)
    home_city_entry = ttk.Entry(dialog)
    home_city_entry.grid(row=3, column=1, padx=5, pady=5)

    team_size_label = ttk.Label(dialog, text="Team Size:")
    team_size_label.grid(row=4, column=0, padx=5, pady=5)
    team_size_entry = ttk.Entry(dialog)
    team_size_entry.grid(row=4, column=1, padx=5, pady=5)

    position_label = ttk.Label(dialog, text="Position:")
    position_label.grid(row=5, column=0, padx=5, pady=5)
    position_entry = ttk.Entry(dialog)
    position_entry.grid(row=5, column=1, padx=5, pady=5)

    def delete_player():
        full_name: str = full_name_entry.get()
        birth_date: str = birth_date_entry.get()
        football_team: str = football_team_entry.get()
        home_city: str = home_city_entry.get()
        team_size: str = team_size_entry.get()
        position: str = position_entry.get()
        delete_num: int = 0
        if is_database is True:
            if full_name:
                delete_num += db_player_controller.delete_by_full_name(full_name)
            if birth_date:
                try:
                    delete_num += db_player_controller.delete_by_birth_date(
                        datetime.datetime.strptime(birth_date, "%Y-%m-%d").date())
                except ValueError:
                    show_error("Ошибка: Некорректный формат даты. Используйте формат 'YYYY-MM-DD'.")
                    return
            if football_team:
                delete_num += db_player_controller.delete_by_football_team(football_team)
            if home_city:
                delete_num += db_player_controller.delete_by_home_city(home_city)
            if team_size:
                try:
                    delete_num += db_player_controller.delete_by_team_size(int(team_size))
                except ValueError:
                    show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
                    return
            if position:
                delete_num += db_player_controller.delete_by_position(position)
        else:
            if full_name:
                delete_num += xml_player_controller.delete_by_name(full_name)
            if birth_date:
                delete_num += xml_player_controller.delete_by_birth_date(birth_date)
            if football_team:
                delete_num += xml_player_controller.delete_by_football_team(football_team)
            if home_city:
                delete_num += xml_player_controller.delete_by_home_city(home_city)
            if team_size:
                try:
                    delete_num += xml_player_controller.delete_by_team_size(int(team_size))
                except ValueError:
                    show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
                    return
            if position:
                delete_num += xml_player_controller.delete_by_position(position)
        messagebox.showinfo("Успех!", "Удалено игроков: " + str(delete_num))
        dialog.destroy()

    delete = ttk.Button(dialog, text="Delete Player", command=delete_player)
    delete.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


root = tk.Tk()
root.title("Library App")
root.geometry('1470x720')

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open a db file", command=set_is_database_true)
file_menu.add_command(label="Open an XML file", command=set_is_database_false)
file_menu.add_command(label="Save file", command=save)
file_menu.add_command(label="Exit", command=on_exit)
menu_bar.add_cascade(label="File", menu=file_menu)

view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Find", command=lambda: SearchWindow(root))
view_menu.add_command(label="Tree", command=lambda: show_tree_window())
menu_bar.add_cascade(label="View", menu=view_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Create", command=create_player)
edit_menu.add_command(label="Delete", command=delete_players)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

create_button = ttk.Button(toolbar, text="Create Player", command=create_player)
create_button.pack(side=tk.LEFT, padx=2, pady=2)
delete_button = ttk.Button(toolbar, text="Delete Player", command=delete_players)
delete_button.pack(side=tk.LEFT)

root.config(menu=menu_bar)

navigation_frame = tk.Frame(root)
navigation_frame.pack()

info_frame = tk.Frame(root)
info_frame.pack()

columns = ("ID", "Full Name", "Birth Date", "Football Team", "Home City", "Team Size", "Position")
column_widths = (100, 150, 100, 120, 100, 80, 100)  # Ширина каждого столбца

current_page = 1
records_per_page = 10

prev_button = tk.Button(navigation_frame, text="Previous", command=prev_page)
prev_button.pack(side=tk.LEFT)

next_button = tk.Button(navigation_frame, text="Next", command=next_page)
next_button.pack(side=tk.LEFT)

first_button = tk.Button(navigation_frame, text="First", command=first_page)
first_button.pack(side=tk.LEFT)

last_button = tk.Button(navigation_frame, text="Last", command=last_page)
last_button.pack(side=tk.LEFT)

total_records_label = tk.Label(info_frame, text="Total Records: {}".format(calculate_total_records()))
total_records_label.pack()

total_pages_label = tk.Label(info_frame, text="Total Pages: {}".format(calculate_total_pages()))
total_pages_label.pack()

current_page_label = tk.Label(info_frame, text="Current Page: {}".format(current_page))
current_page_label.pack()

records_per_page_label = tk.Label(info_frame, text="Records per Page: {}".format(records_per_page))
records_per_page_label.pack()

records_per_page_entry = tk.Entry(info_frame)
records_per_page_entry.pack(side=tk.LEFT)
records_per_page_entry.insert(0, "10")

change_records_per_page_button = tk.Button(info_frame, text="Change", command=change_records_per_page)
change_records_per_page_button.pack(side=tk.LEFT)

treeview = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, anchor="center")
treeview.pack()

display_players()

root.mainloop()
