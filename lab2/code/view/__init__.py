# import datetime
#
# from controller.DB import DBPlayerController
# from controller.XML import XmlPlayerController
# from controller.PlayerDto import PlayerDto
#
# from entity.Player import Player
#
# player = Player()
# player.id = 52
# player.full_name = 'Q'
# player.birth_date = datetime.date(2020, 12, 12)
# player.football_team = 'Q'
# player.home_city = 'Q'
# player.team_size = 11
# player.position = 'Q'
#
# player2 = PlayerDto(full_name='B', football_team='B', position='B', id=52, home_city='b', birth_date=datetime.date(
#     1230, 1, 12), team_size=123)
#
# player_controller = DBPlayerController()
# my_tuple_for_find_all = player_controller.get_all()
# for item in my_tuple_for_find_all:
#     print(item)
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.get_by_id(32))
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.get_by_position("Defender"))
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# my_tuple_for_team_size = player_controller.get_by_team_size(11)
# for item in my_tuple_for_team_size:
#     print(item)
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.get_by_birth_date(datetime.date(1992, 6, 26)))
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.get_by_full_name("John"))
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.get_by_football_team("Red Bull Salzburg"))
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.get_by_home_city("Minsk"))
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#
# player_controller.delete_by_position("Defender")
# player_controller.delete_by_full_name("John")
# player_controller.delete_by_home_city("Minsk")
# player_controller.delete_by_football_team("PFC Ludogorets Razgrad")
# player_controller.delete_by_birth_date(datetime.date(1230, 1, 12))
# player_controller.delete_by_team_size(11)
#
# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.create(player2))
# player_controller.save_db()
# print(player_controller.update(player2))
# # Создаем экземпляр хранилища XML
# xml_storage = XmlPlayerController("C:/Users/Daniil/PycharmProjects/ppois-2-2024/lab2/players.xml")
#
# # Выводим всех игроков из XML
# print("All players from XML:")
# all_players = xml_storage.get_all_players()
# for player in all_players:
#     print(player)
#
# # Добавляем нового игрока
# new_player = Player(51, "Michael Jordan", datetime.date(1111, 11, 11), "Chicago Bulls", "New York", 5, "Guard")
# xml_storage.insert(new_player)
# print("\nAdded player:")
# print(new_player)
#
# # Сохраняем изменения в XML
# xml_storage.save()
# print("\nChanges saved to XML.")
#
# # Поиск игрока по имени
# name_to_search = "Jordan"
# found_players_by_name = xml_storage.search_by_name(name_to_search)
# print(f"\nPlayers found by name '{name_to_search}':")
# for player in found_players_by_name:
#     print(player)
#
# # Удаление игрока по имени
# num_deleted_by_name = xml_storage.delete_by_name(name_to_search)
# print(f"\nNumber of players deleted by name '{name_to_search}': {num_deleted_by_name}")
#
#
# Поиск игрока по футбольной команде
# team_to_search = "AS Roma"
# found_players_by_team = xml_storage.search_by_football_team(team_to_search)
# print(f"\nPlayers found by team '{team_to_search}':")
# for player in found_players_by_team:
#     print(player)
#
# Удаление игрока по футбольной команде
# num_deleted_by_team = xml_storage.delete_by_football_team(team_to_search)
# print(f"\nNumber of players deleted by team '{team_to_search}': {num_deleted_by_team}")
#
# # Поиск игрока по позиции
# position_to_search = "Defender"
# found_players_by_position = xml_storage.search_by_position(position_to_search)
# print(f"\nPlayers found by position '{position_to_search}':")
# for player in found_players_by_position:
#     print(player)
#
# Удаление игрока по позиции
# num_deleted_by_position = xml_storage.delete_by_position(position_to_search)
# print(f"\nNumber of players deleted by position '{position_to_search}': {num_deleted_by_position}")
#
#
# # Выводим всех игроков после удалений
# print("\nAll players after deletions:")
# updated_players = xml_storage.get_all_players()
# for player in updated_players:
#     print(player)
#
# from controller.XML import XmlPlayerController
# from controller.DB import DBPlayerController
# import tkinter as tk
# from tkinter import ttk
#
# xml_controller = XmlPlayerController("C:/Users/Daniil/PycharmProjects/ppois-2-2024/lab2"
#                                      "/players.xml")
# db_controller = DBPlayerController()
# is_database = True
# data = db_controller.get_all()
#
#
# def display_players():
#     global current_page, records_per_page, treeview, data
#
#     # Очищаем все данные в таблице перед обновлением
#     for row in treeview.get_children():
#         treeview.delete(row)
#
#     # Определяем, откуда получать данные: из базы данных или из XML
#     if is_database:
#         # Получаем данные из базы данных
#         data = db_controller.get_all()
#     else:
#         data = xml_controller.get_all_players()
#
#     # Добавляем данные в таблицу
#     start = (current_page - 1) * records_per_page
#     end = start + records_per_page
#     for player in data[start:end]:
#         record = (
#             player.id, player.full_name, player.birth_date, player.football_team, player.home_city, player.team_size,
#             player.position)
#         treeview.insert("", "end", values=record)
#
#
# def calculate_total_pages():
#     global records_per_page, data
#     return -(-len(data) // records_per_page)
#
#
# def prev_page():
#     global current_page
#     if current_page > 1:
#         current_page -= 1
#         display_players()
#         update_page_info()
#
#
# def next_page():
#     global current_page
#     total_pages = calculate_total_pages()
#     if current_page < total_pages:
#         current_page += 1
#         display_players()
#         update_page_info()
#
#
# def first_page():
#     global current_page
#     if current_page != 1:
#         current_page = 1
#         display_players()
#         update_page_info()
#
#
# def last_page():
#     global current_page
#     total_pages = calculate_total_pages()
#     if current_page != total_pages:
#         current_page = total_pages
#         display_players()
#         update_page_info()
#
#
# def change_records_per_page():
#     global records_per_page
#     try:
#         new_records_per_page = int(records_per_page_entry.get())
#         if new_records_per_page > 0:
#             records_per_page = new_records_per_page
#             display_players()
#             update_page_info()
#     except ValueError:
#         pass
#
#
# def update_page_info():
#     global current_page, records_per_page, treeview
#     total_pages_label.config(text="Total Pages: {}".format(calculate_total_pages()))
#     current_page_label.config(text="Current Page: {}".format(current_page))
#     records_per_page_label.config(text="Records per Page: {}".format(records_per_page))
#     total_records_label.config(text="Total Records: {}".format(calculate_total_records()))
#
#
# def calculate_total_records():
#     return len(data)
#
#
# def set_is_database_true():
#     global is_database
#     is_database = True
#     first_page()
#
#
# def set_is_database_false():
#     global is_database
#     is_database = False
#     first_page()
#
#
# # Main code
# root = tk.Tk()
# root.title("Pagination App")
# root.geometry('1470x720')
#
# # Создаем меню
# menu_bar = tk.Menu(root)
#
# # Создаем меню "File" и добавляем в него пункты
# file_menu = tk.Menu(menu_bar, tearoff=0)
# file_menu.add_command(label="Open a db file", command=set_is_database_true)
# file_menu.add_command(label="Open an XML file", command=set_is_database_false)
# menu_bar.add_cascade(label="File", menu=file_menu)
#
# # Устанавливаем меню приложения
# root.config(menu=menu_bar)
#
# # Создаем фреймы для кнопок навигации и информации
# navigation_frame = tk.Frame(root)
# navigation_frame.pack()
#
# info_frame = tk.Frame(root)
# info_frame.pack()
#
# columns = ("ID", "Full Name", "Birth Date", "Football Team", "Home City", "Team Size", "Position")
# column_widths = (100, 150, 100, 120, 100, 80, 100)  # Ширина каждого столбца
#
# current_page = 1
# records_per_page = 10
#
# # Кнопки навигации
# prev_button = tk.Button(navigation_frame, text="Previous", command=prev_page)
# prev_button.pack(side=tk.LEFT)
#
# next_button = tk.Button(navigation_frame, text="Next", command=next_page)
# next_button.pack(side=tk.LEFT)
#
# first_button = tk.Button(navigation_frame, text="First", command=first_page)
# first_button.pack(side=tk.LEFT)
#
# last_button = tk.Button(navigation_frame, text="Last", command=last_page)
# last_button.pack(side=tk.LEFT)
#
# # Надписи с информацией
# total_records_label = tk.Label(info_frame, text="Total Records: {}".format(calculate_total_records()))
# total_records_label.pack()
#
# total_pages_label = tk.Label(info_frame, text="Total Pages: {}".format(calculate_total_pages()))
# total_pages_label.pack()
#
# current_page_label = tk.Label(info_frame, text="Current Page: {}".format(current_page))
# current_page_label.pack()
#
# records_per_page_label = tk.Label(info_frame, text="Records per Page: {}".format(records_per_page))
# records_per_page_label.pack()
#
# records_per_page_entry = tk.Entry(info_frame)
# records_per_page_entry.pack(side=tk.LEFT)
# records_per_page_entry.insert(0, "10")
#
# change_records_per_page_button = tk.Button(info_frame, text="Change", command=change_records_per_page)
# change_records_per_page_button.pack(side=tk.LEFT)
#
# treeview = ttk.Treeview(root, columns=columns, show="headings")
# for col in columns:
#     treeview.heading(col, text=col)
#     treeview.column(col, anchor="center")
# treeview.pack()
#
# display_players()
#
# root.mainloop()
from anytree import Node, RenderTree
from typing import List
import datetime

from model.entity.Player import Player
from controller.DB import DBPlayerController
db_controller = DBPlayerController()
# Пример списка игроков
players = db_controller.get_all()

# Создаем корневой узел для древовидной структуры
root = Node("Players")

# Проходим по каждому игроку в списке
for player in players:
    # Создаем узел для каждого игрока с его уникальным идентификатором
    player_node = Node(str(player.id), parent=root)
    # Добавляем дочерние узлы с атрибутами игрока
    Node(f"id: {player.id}", parent=player_node)
    Node(f"full_name: {player.full_name}", parent=player_node)
    Node(f"birth_date: {player.birth_date}", parent=player_node)
    Node(f"football_team: {player.football_team}", parent=player_node)
    Node(f"home_city: {player.home_city}", parent=player_node)
    Node(f"team_size: {player.team_size}", parent=player_node)
    Node(f"position: {player.position}", parent=player_node)

# Выводим древовидную структуру
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
