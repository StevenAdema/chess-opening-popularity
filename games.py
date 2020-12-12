import sqlite3
import pandas as pd
import os


class Games:
    """An object which contains a record chess games

    Reads chess game metadata from a database allowing a custom
    selection that can be filtered by opening moves and elo. Also calculates
    the relative daily popularity of every 3 move opening.

    Attributes:
        opening: the 3 opening moves played in the game
        opening_name: the plain text name for the opening (if available)
        elo: the elo band to filter the results on
        conn: connection to sqlite3 database
        cursor: cursor to execute transactions on the database
        df: a DataFrame object containing the chess games, openings of interest
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, db_name, opening=None, elo=None, opening_name=None):
        """ Initialize a Games object containing filtered chess game metadata

        Args:
            db_name (str): name of the database with chess game metadata.
            opening (str, optional): the 3 set move to filter the results by
            elo (str, optional): the elo band to filter the results on
            opening_name (str, option): the plain text name of the opening line
        """
        self.opening = opening
        self.opening_name = opening_name
        self.elo = elo
        self.db_name = os.path.dirname(__file__) + db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.df = Games.generate_games_df(self, self.opening, self.elo)
        Games.calculate_daily_opening_popularity(self)
        self.conn.commit()
        self.conn.close()

    def generate_games_df(self, opening=None, elo=None):
        """Read from database to DataFrame attribute the games and openings of interest"""
        query = 'select * from lichess_openings_summary'
        if opening is not None and elo is not None:
            query = query + ' WHERE opening="' + opening + '" AND WhiteELO="' + elo + '"'
        elif opening is not None:
            query = query + ' WHERE opening="' + opening + '"'
        elif elo is not None:
            query = query + ' WHERE WhiteELO="' + elo + '"'

        df = pd.read_sql_query(query, self.conn)
        return df

    def calculate_daily_opening_popularity(self):
        """calculate the relative popularity of each opening"""
        self.df['opening_percentage_played'] = 100 * (self.df['openingCount'] / self.df['dailyGamesSum'])