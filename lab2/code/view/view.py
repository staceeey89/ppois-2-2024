import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from controller.DB import DBPlayerController
from controller.PlayerDto import PlayerDto
from controller.XML import XmlPlayerController

db_player_controller: DBPlayerController = DBPlayerController()
xml_player_controller: XmlPlayerController = XmlPlayerController("C:/Users/Daniil/PycharmProjects/ppois-2-2024/lab2"
                                                                 "/players.xml")


def show_error(message):
    messagebox.showerror("Ошибка", message)


def save_db():
    if messagebox.askyesno("Сохранение", "Вы хотите сохранить изменение базы данных?"):
        db_player_controller.save_db()


def on_exit():
    if messagebox.askyesno("Выход", "Вы хотите выйти из приложения?"):
        root.destroy()


def validate_input(full_name, birth_date_str, football_team, home_city, team_size_str, position):
    # Проверка full_name
    if not full_name.strip():
        show_error("Ошибка: Поле 'full_name' не должно быть пустым.")
        return False

    # Проверка birth_date
    try:
        datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")
    except ValueError:
        show_error("Ошибка: Некорректный формат даты. Используйте формат 'YYYY-MM-DD'.")
        return False

    # Проверка football_team, home_city, position
    if not football_team.strip():
        show_error("Ошибка: Поле 'football_team' не должно быть пустым.")
        return False
    if not home_city.strip():
        show_error("Ошибка: Поле 'home_city' не должно быть пустым.")
        return False
    if not position.strip():
        show_error("Ошибка: Поле 'position' не должно быть пустым.")
        return False

    # Проверка team_size
    team_size_str = team_size_str.strip()
    if not team_size_str.isdigit():
        show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
        return False

    return True


def display_players():
    # Очищаем все данные в таблице перед обновлением
    for row in treeview.get_children():
        treeview.delete(row)

    # Получаем данные из базы данных
    players = db_player_controller.get_all()

    # Добавляем данные в таблицу
    for player in players:
        treeview.insert("", "end", values=(
            player.id, player.full_name, player.birth_date, player.football_team, player.home_city, player.team_size,
            player.position))


def create_player():
    # Создаем новое диалоговое окно
    dialog = tk.Toplevel(root)
    dialog.title("Create Player")
    dialog.grab_set()  # Блокируем доступ к другим окнам

    # Добавляем метки и поля ввода для данных игрока
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
        # Получаем значения из полей ввода
        full_name: str = full_name_entry.get()
        birth_date: str = birth_date_entry.get()
        football_team: str = football_team_entry.get()
        home_city: str = home_city_entry.get()
        team_size: str = team_size_entry.get()
        position: str = position_entry.get()

        if validate_input(full_name, birth_date, football_team, home_city, team_size, position):
            team_size: int = int(team_size_entry.get())
            birth_date: datetime.date = datetime.datetime.strptime(birth_date_entry.get(), "%Y-%m-%d")

            # Создаем новый объект игрока
            new_player = PlayerDto(full_name=full_name, birth_date=birth_date, football_team=football_team,
                                   home_city=home_city, team_size=team_size, position=position, id=None)

            # Добавляем игрока в базу данных
            player_id = db_player_controller.create(new_player)

            # Выводим сообщение об успешном добавлении
            messagebox.showinfo("Успех!", f"Игрок с ID {player_id.id} успешно создан!.")
            dialog.destroy()

    # Кнопка "Сохранить игрока"
    save_button = ttk.Button(dialog, text="Save Player", command=save_player)
    save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


root = tk.Tk()
root.title("Library App")
root.geometry('1470x720')

# Создаем меню
menu_bar = tk.Menu(root)

# Создаем меню "File" и добавляем в него пункты
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save DB", command=save_db)
file_menu.add_command(label="Exit", command=on_exit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Создаем панель инструментов
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Кнопка "Create Player"
create_button = ttk.Button(toolbar, text="Create Player", command=create_player)
create_button.pack(side=tk.LEFT, padx=2, pady=2)

# Устанавливаем меню приложения
root.config(menu=menu_bar)

# Создаем виджет Treeview для отображения данных в виде таблицы
columns = ("ID", "Full Name", "Birth Date", "Football Team", "Home City", "Team Size", "Position")
treeview = ttk.Treeview(root, columns=columns, show="headings")

# Устанавливаем заголовки столбцов
for col in columns:
    treeview.heading(col, text=col)

# Растягиваем столбцы для лучшего отображения
for col in columns:
    treeview.column(col, anchor="center")

# Устанавливаем вертикальную прокрутку
scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)

# Кнопка для обновления данных
update_button = tk.Button(root, text="Update", command=display_players)

# Размещаем виджеты на форме
treeview.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
update_button.pack()

# Инициализируем отображение данных
display_players()

root.mainloop()
