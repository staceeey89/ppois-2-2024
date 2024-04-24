from sqlite3 import connect
from typing import List

from extras.tournament import Tournament
from src.model import Model


class SqlStorage(Model):
    def __init__(self) -> None:
        super().__init__()
        self.conn = connect('data/tournaments.db')
        self._protected_create_table()

    def __del__(self):
        self.conn.close()

    def __len__(self):
        return len(self.get_all_tournaments(limit=100))

    def _protected_create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY NOT NULL,
                TrnName TEXT NOT NULL,
                TrnDate TEXT NOT NULL,
                TrnSport TEXT NOT NULL,
                WinName TEXT NOT NULL,
                TrnPrize INTEGER NOT NULL,
                WinPrize INTEGER NOT NULL
            )
        ''')

    def insert(self, tournament: Tournament):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tournaments (
                TrnName, 
                TrnDate, 
                TrnSport, 
                WinName, 
                TrnPrize, 
                WinPrize) 
            VALUES (?, ?, ?, ?, ?, ?)''',
                       (tournament.trn_name,
                        tournament.trn_date,
                        tournament.trn_sport,
                        tournament.win_name,
                        tournament.trn_prize,
                        tournament.win_prize))

    def get_all_tournaments(self, offset=0, limit=None) -> List[Tournament]:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM tournaments''')
        rows = cursor.fetchall()
        tournaments: List = []
        for row in rows:
            tournament = Tournament(*row)
            tournaments.append(tournament)
        return tournaments[offset: offset + limit]

    def get_all_sports(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT TrnSport FROM tournaments''')
        rows = cursor.fetchall()
        sports = sorted({sport[0] for sport in rows})
        return sports

    def search_by_trn_name(self, trn_name: str, offset=0, limit=None) -> List[Tournament]:
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM tournaments WHERE TrnName LIKE ?'''
        cursor.execute(query, ('%' + trn_name + '%',))

        query = '''SELECT * FROM tournaments WHERE TrnName LIKE ? LIMIT ? OFFSET ?'''
        cursor.execute(query, ('%' + trn_name + '%', limit, offset))
        rows = cursor.fetchall()

        tournaments = []
        for row in rows:
            tournament = Tournament(*row)
            tournaments.append(tournament)
        return tournaments

    def delete_by_trn_name(self, trn_name: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM tournaments WHERE TrnName LIKE ?''', ('%' + trn_name + '%',))
        deleted_count = cursor.rowcount
        return deleted_count

    def search_by_trn_sport(self, trn_sport: str, offset=0, limit=None) -> List[Tournament]:
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM tournaments WHERE TrnSport LIKE ?'''
        cursor.execute(query, ('%' + trn_sport + '%',))
        # total_count = cursor.fetchone()[0]

        query = '''SELECT * FROM tournaments WHERE TrnSport LIKE ? LIMIT ? OFFSET ?'''
        cursor.execute(query, ('%' + trn_sport + '%', limit, offset))
        rows = cursor.fetchall()

        tournaments = []
        for row in rows:
            tournament = Tournament(*row)
            tournaments.append(tournament)
        # is it necessary to return  (tournaments, total_count) ?
        return tournaments

    def delete_by_trn_sport(self, trn_sport: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM tournaments WHERE TrnSport LIKE ?''', ('%' + trn_sport + '%',))
        deleted_count = cursor.rowcount
        return deleted_count

    def search_by_trn_prize(self, bottom: int, top: int, offset=0, limit=None) -> List[Tournament]:
        cursor = self.conn.cursor()
        query = '''SELECT COUNT(*) FROM tournaments WHERE TrnPrize BETWEEN ? AND ?'''
        cursor.execute(query, (bottom, top))
        # total_count = cursor.fetchone()[0]

        query = '''SELECT * FROM tournaments WHERE TrnPrize BETWEEN ? AND ? LIMIT ? OFFSET ?'''
        cursor.execute(query, (bottom, top, limit, offset))
        rows = cursor.fetchall()

        tournaments = []
        for row in rows:
            tournament = Tournament(*row)
            tournaments.append(tournament)
        # is it necessary to return  (tournaments, total_count) ?
        return tournaments

    def delete_by_trn_prize(self, bottom: int, top: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM tournaments WHERE TrnPrize BETWEEN ? AND ?''', (bottom, top))
        deleted_count = cursor.rowcount
        return deleted_count

    def save(self) -> None:
        self.conn.commit()
