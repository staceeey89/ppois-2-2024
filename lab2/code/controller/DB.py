import datetime
from typing import List

from model.Model import PlayerDao
from controller.PlayerDto import PlayerDto
from model.entity.Player import Player


def to_player_dto(player: Player) -> PlayerDto:
    player_dto: PlayerDto = PlayerDto(full_name=player.full_name, team_size=player.team_size,
                                      home_city=player.home_city, birth_date=player.birth_date,
                                      football_team=player.football_team, position=player.position, id=player.id)
    return player_dto


def to_player_entity(player_dto: PlayerDto) -> Player:
    player: Player = Player(home_city=player_dto.home_city, birth_date=player_dto.birth_date,
                            position=player_dto.position, football_team=player_dto.football_team,
                            team_size=player_dto.team_size, full_name=player_dto.full_name, id=None)
    return player


class DBPlayerController:
    def __init__(self):
        self.__player_dao = PlayerDao()

    def get_by_id(self, player_id: int) -> PlayerDto:
        player: Player = self.__player_dao.find_by_id(player_id)
        if player is None:
            raise RuntimeWarning("No player with id: " + str(player_id))
        return to_player_dto(player)

    def get_all(self) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_all()
        player_dtos: List[PlayerDto] = [to_player_dto(player) for player in players]
        return player_dtos

    def get_by_full_name(self, name: str) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_by_full_name(name)
        if players is None:
            raise RuntimeWarning("No players with name: " + name)
        return [to_player_dto(player) for player in players]

    def get_by_birth_date(self, date: datetime.date) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_by_birth_date(date)
        if players is None:
            raise RuntimeWarning("No players with birth date: " + date.strftime('%Y-%m-%d'))
        return [to_player_dto(player) for player in players]

    def get_by_position(self, position: str) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_by_position(position)
        if players is None:
            raise RuntimeWarning("No players with position: " + position)
        return [to_player_dto(player) for player in players]

    def get_by_team_size(self, size: int) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_by_team_size(size)
        if players is None:
            raise RuntimeWarning("No players with team size : " + str(size))
        return [to_player_dto(player) for player in players]

    def get_by_football_team(self, team_name: str) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_by_football_team(team_name)
        if players is None:
            raise RuntimeWarning("No players with football team: " + team_name)
        return [to_player_dto(player) for player in players]

    def get_by_home_city(self, home: str) -> List[PlayerDto]:
        players: List[Player] = self.__player_dao.find_by_home_city(home)
        if players is None:
            raise RuntimeWarning("No players with home city: " + home)
        return [to_player_dto(player) for player in players]

    def delete_by_full_name(self, name: str):
        players: List[Player] = self.__player_dao.find_by_full_name(name)
        if players is None:
            raise RuntimeWarning("Players with name " + name + " not found")
        print(self.__player_dao.delete_by_full_name(name))

    def delete_by_birth_date(self, date: datetime.date):
        players: List[Player] = self.__player_dao.find_by_birth_date(date)
        if players is None:
            raise RuntimeWarning("Players with birth date " + date.strftime('%Y-%m-%d') + " not found")
        print(self.__player_dao.delete_by_birth_date(date))

    def delete_by_football_team(self, team_name: str):
        players: List[Player] = self.__player_dao.find_by_football_team(team_name)
        if players is None:
            raise RuntimeWarning("Players with football team " + team_name + " not found")
        print(self.__player_dao.delete_by_football_team(team_name))

    def delete_by_home_city(self, home: str):
        players: List[Player] = self.__player_dao.find_by_home_city(home)
        if players is None:
            raise RuntimeWarning("Players with home city " + home + " not found")
        print(self.__player_dao.delete_by_home_city(home))

    def delete_by_team_size(self, size: int):
        players: List[Player] = self.__player_dao.find_by_team_size(size)
        if players is None:
            raise RuntimeWarning("Players with team size " + str(size) + " not found")
        print(self.__player_dao.delete_by_team_size(size))

    def delete_by_position(self, position: str):
        players: List[Player] = self.__player_dao.find_by_position(position)
        if players is None:
            raise RuntimeWarning("Players with position " + position + " not found")
        print(self.__player_dao.delete_by_position(position))

    def update(self, dto: PlayerDto) -> PlayerDto:
        player: Player = to_player_entity(dto)
        player.id = dto.id
        player_created: Player = self.__player_dao.update(player)
        if player_created is None:
            raise RuntimeWarning("No player with id: " + str(dto.id))
        return to_player_dto(player_created)

    def create(self, dto: PlayerDto) -> PlayerDto:
        player: Player = to_player_entity(dto)
        player_created: Player = self.__player_dao.create(player)
        return to_player_dto(player_created)

    def save_db(self):
        self.__player_dao.save_db()
