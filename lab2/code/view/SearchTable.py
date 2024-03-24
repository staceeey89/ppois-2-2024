import tkinter as tk
from tkinter import ttk


class SearchResultsWindow:
    def __init__(self, parent, results):
        self.parent = parent
        self.results = results

        # Создание нового окна для отображения результатов поиска
        self.window = tk.Toplevel(parent)
        self.window.title("Результаты поиска")

        # Создание виджета Treeview для отображения результатов поиска
        columns = ("ID", "Full Name", "Birth Date", "Football Team", "Home City", "Team Size", "Position")
        self.treeview = ttk.Treeview(self.window, columns=columns, show="headings")

        # Установка заголовков столбцов
        for col in columns:
            self.treeview.heading(col, text=col)

        # Растягиваем столбцы для лучшего отображения
        for col in columns:
            self.treeview.column(col, anchor="center")

        # Добавляем данные в таблицу
        for player in results:
            self.treeview.insert("", "end", values=(
                player.id, player.full_name, player.birth_date, player.football_team, player.home_city,
                player.team_size, player.position))

        # Создаем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Размещаем виджеты на форме
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
#
# def show_error(message):
#     messagebox.showerror("Ошибка", message)
#
#
# class SearchWindow:
#     def __init__(self, parent):
#         self.parent = parent
#         self.window = tk.Toplevel(parent)
#         self.window.title("Поиск")
#         self.window.grab_set()
#
#         self.full_name_label = ttk.Label(self.window, text="Full Name:")
#         self.full_name_label.grid(row=0, column=0, padx=5, pady=5)
#         self.full_name_entry = ttk.Entry(self.window)
#         self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)
#
#         self.birth_date_label = ttk.Label(self.window, text="Birth Date (YYYY-MM-DD):")
#         self.birth_date_label.grid(row=1, column=0, padx=5, pady=5)
#         self.birth_date_entry = ttk.Entry(self.window)
#         self.birth_date_entry.grid(row=1, column=1, padx=5, pady=5)
#
#         self.football_team_label = ttk.Label(self.window, text="Football Team:")
#         self.football_team_label.grid(row=2, column=0, padx=5, pady=5)
#         self.football_team_entry = ttk.Entry(self.window)
#         self.football_team_entry.grid(row=2, column=1, padx=5, pady=5)
#
#         self.home_city_label = ttk.Label(self.window, text="Home City:")
#         self.home_city_label.grid(row=3, column=0, padx=5, pady=5)
#         self.home_city_entry = ttk.Entry(self.window)
#         self.home_city_entry.grid(row=3, column=1, padx=5, pady=5)
#
#         self.team_size_label = ttk.Label(self.window, text="Team Size:")
#         self.team_size_label.grid(row=4, column=0, padx=5, pady=5)
#         self.team_size_entry = ttk.Entry(self.window)
#         self.team_size_entry.grid(row=4, column=1, padx=5, pady=5)
#
#         self.position_label = ttk.Label(self.window, text="Position:")
#         self.position_label.grid(row=5, column=0, padx=5, pady=5)
#         self.position_entry = ttk.Entry(self.window)
#         self.position_entry.grid(row=5, column=1, padx=5, pady=5)
#
#         self.search_button = ttk.Button(self.window, text="Найти", command=self.search)
#         self.search_button.grid(row=0, column=2, padx=5, pady=5)
#
#     def search(self):
#         full_name: str = self.full_name_entry.get()
#         birth_date: str = self.birth_date_entry.get()
#         football_team: str = self.football_team_entry.get()
#         home_city: str = self.home_city_entry.get()
#         team_size: str = self.team_size_entry.get()
#         position: str = self.position_entry.get()
#         if is_database is True:
#             found_players = db_controller.get_all()
#             if full_name:
#                 found_players = set(db_controller.get_by_full_name(full_name))
#             if birth_date:
#                 try:
#                     found_players = set(found_players) & set(
#                         db_controller.get_by_birth_date(datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()))
#                 except ValueError:
#                     show_error("Ошибка: Некорректный формат даты. Используйте формат 'YYYY-MM-DD'.")
#                     return
#             if football_team:
#                 found_players = set(found_players) & set(db_controller.get_by_football_team(football_team))
#             if home_city:
#                 found_players = set(found_players) & set(db_controller.get_by_home_city(home_city))
#             if team_size:
#                 try:
#                     found_players = set(found_players) & set(db_controller.get_by_team_size(int(team_size)))
#                 except ValueError:
#                     show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
#                     return
#             if position:
#                 found_players = set(found_players) & set(db_controller.get_by_position(position))
#         else:
#             found_players = xml_controller.get_all_players()
#             if full_name:
#                 found_players = set(xml_controller.search_by_name(full_name))
#             if birth_date:
#                 found_players = set(found_players) & set(xml_controller.search_by_birth_date(birth_date))
#             if football_team:
#                 found_players = set(found_players) & set(xml_controller.search_by_football_team(football_team))
#             if home_city:
#                 found_players = set(found_players) & set(xml_controller.search_by_home_city(home_city))
#             if team_size:
#                 try:
#                     found_players = set(found_players) & set(xml_controller.search_by_team_size(int(team_size)))
#                 except ValueError:
#                     show_error("Ошибка: Поле 'team_size' должно содержать только цифры.")
#                     return
#             if position:
#                 found_players = set(found_players) & set(xml_controller.search_by_position(position))
#         found_players = list(found_players)
#         SearchResultsWindow(self.window, found_players)
#
#
# class SearchResultsWindow:
#     def __init__(self, parent, results):
#         self.parent = parent
#         self.results = results
#
#         # Создание нового окна для отображения результатов поиска
#         self.window = tk.Toplevel(parent)
#         self.window.title("Результаты поиска")
#
#         # Создание виджета Treeview для отображения результатов поиска
#         columns = ("ID", "Full Name", "Birth Date", "Football Team", "Home City", "Team Size", "Position")
#         self.treeview = ttk.Treeview(self.window, columns=columns, show="headings")
#
#         # Установка заголовков столбцов
#         for col in columns:
#             self.treeview.heading(col, text=col)
#
#         # Растягиваем столбцы для лучшего отображения
#         for col in columns:
#             self.treeview.column(col, anchor="center")
#
#         # Добавляем данные в таблицу
#         for player in results:
#             self.treeview.insert("", "end", values=(
#                 player.id, player.full_name, player.birth_date, player.football_team, player.home_city,
#                 player.team_size, player.position))
#
#         # Создаем вертикальную прокрутку
#         scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.treeview.yview)
#         self.treeview.configure(yscrollcommand=scrollbar.set)
#
#         # Размещаем виджеты на форме
#         self.treeview.pack(side="left", fill="both", expand=True)
#         scrollbar.pack(side="right", fill="y")
