from typing import List

import psycopg2
import datetime

from model.entity.Player import Player


class PlayerDao:
    def __init__(self):
        try:
            self.__connection = psycopg2.connect('postgresql://postgres:root@127.0.0.1:5432/ppois2')
        except UnicodeDecodeError:
            print('Can`t establish connection to database')
        self.__find_by_id_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, p.team_size, '
                                   'p.position FROM players p WHERE p.id = %s')
        self.__find_all_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, p.team_size, '
                                 'p.position FROM players p')
        self.__find_by_full_name_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, '
                                          'p.team_size, p.position FROM players p WHERE full_name LIKE %s')
        self.__find_by_birth_date_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, '
                                           'p.team_size, p.position FROM players p WHERE birth_date = %s')
        self.__find_by_position_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, '
                                         'p.team_size, p.position FROM players p WHERE position = %s')
        self.__find_by_team_size_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, '
                                          'p.team_size, p.position FROM players p WHERE '
                                          'team_size = %s')
        self.__find_by_football_team_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, '
                                              'p.team_size, p.position FROM players p WHERE '
                                              'football_team = %s')
        self.__find_by_home_city_query = ('SELECT p.id, p.full_name, p.birth_date, p.football_team, p.home_city, '
                                          'p.team_size, p.position FROM players p WHERE '
                                          'home_city = %s')
        self.__delete_by_full_name_query = 'DELETE FROM players WHERE full_name LIKE %s'
        self.__delete_by_birth_date_query = 'DELETE FROM players WHERE birth_date = %s'
        self.__delete_by_football_team_query = 'DELETE FROM players WHERE football_team = %s'
        self.__delete_by_home_city_query = 'DELETE FROM players WHERE home_city = %s'
        self.__delete_by_team_size_query = 'DELETE FROM players WHERE team_size = %s'
        self.__delete_by_position_query = 'DELETE FROM players WHERE position = %s'
        self.__update_by_id_query = ('UPDATE players SET full_name = %s, birth_date = %s, football_team = %s, '
                                     'home_city = %s, team_size = %s, position = %s WHERE id = %s')
        self.__create_query = ('INSERT INTO players (full_name, birth_date, football_team, home_city, team_size, '
                               'position) VALUES (%s, %s, %s, %s, %s, %s)')

    def find_by_id(self, player_id) -> Player | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_id_query, (player_id,))
            query = curs.fetchall()
        if query:
            return Player(*query[0])
        else:
            return None

    def find_all(self) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_all_query)
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def find_by_full_name(self, name: str) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_full_name_query, (f'%{name}%',))
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def find_by_birth_date(self, date: datetime.date) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_birth_date_query, (date,))
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def find_by_position(self, position: str) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_position_query, (position,))
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def find_by_team_size(self, size) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_team_size_query, (size,))
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def find_by_football_team(self, team: str) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_football_team_query, (team,))
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def find_by_home_city(self, home: str) -> List[Player] | None:
        with self.__connection.cursor() as curs:
            curs.execute(self.__find_by_home_city_query, (home,))
            query = curs.fetchall()
        if not query:
            return None
        return [Player(*element) for element in query]

    def delete_by_full_name(self, name: str):
        with self.__connection.cursor() as curs:
            curs.execute(self.__delete_by_full_name_query, (f'%{name}%',))
            # self.__connection.commit()
            return curs.rowcount

    def delete_by_birth_date(self, date: datetime.date):
        with self.__connection.cursor() as curs:
            curs.execute(self.__delete_by_birth_date_query, (date,))
            # self.__connection.commit()
            return curs.rowcount

    def delete_by_football_team(self, team: str):
        with self.__connection.cursor() as curs:
            curs.execute(self.__delete_by_football_team_query, (team,))
            # self.__connection.commit()
            return curs.rowcount

    def delete_by_home_city(self, home: str):
        with self.__connection.cursor() as curs:
            curs.execute(self.__delete_by_home_city_query, (home,))
            # self.__connection.commit()
            return curs.rowcount

    def delete_by_team_size(self, size):
        with self.__connection.cursor() as curs:
            curs.execute(self.__delete_by_team_size_query, (size,))
            # self.__connection.commit()
            return curs.rowcount

    def delete_by_position(self, position: str):
        with self.__connection.cursor() as curs:
            curs.execute(self.__delete_by_position_query, (position,))
            # self.__connection.commit()
            return curs.rowcount

    def update(self, player: Player) -> Player:
        with self.__connection.cursor() as curs:
            curs.execute(self.__update_by_id_query, (player.full_name, player.birth_date, player.football_team,
                                                     player.home_city, player.team_size, player.position, player.id))
            # self.__connection.commit()
            return self.find_by_id(player.id)

    def create(self, player: Player) -> Player:
        with self.__connection.cursor() as curs:
            curs.execute(self.__create_query + ' RETURNING id',
                         (player.full_name, player.birth_date, player.football_team,
                          player.home_city, player.team_size, player.position))
            last_row_id = curs.fetchone()[0]
            # self.__connection.commit()
            curs.execute(self.__find_by_id_query, (last_row_id,))
            created_player = curs.fetchone()
            return Player(*created_player)

    def save_db(self):
        self.__connection.commit()

    def __del__(self):
        self.__connection.close()
