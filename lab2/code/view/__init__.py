import datetime

from controller.DB import DBPlayerController
from controller.XML import XmlPlayerController
from controller.PlayerDto import PlayerDto

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
