from controller.Controller import PlayerController
import datetime
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
player2 = PlayerDto(full_name='B', football_team='B', position='B', id=52, home_city='b', birth_date=datetime.date(1230, 1, 12),
                    team_size=123)

player_controller = PlayerController()
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

# player_controller.delete_by_position("Defender")
# player_controller.delete_by_full_name("John")
# player_controller.delete_by_home_city("Minsk")
# player_controller.delete_by_football_team("PFC Ludogorets Razgrad")
# player_controller.delete_by_birth_date(datetime.date(1997, 1, 8))
# player_controller.delete_by_team_size(11)

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print(player_controller.create(player2))
print(player_controller.update(player2))
