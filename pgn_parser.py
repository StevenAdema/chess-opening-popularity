import os
import tqdm
import sqlite3


class PGNs:
    """Create a sqlite database of recorded chess games with relevant metadata
    from a provided pgn (Portable Game Notation) file
    """
    default_pgn = '/data/sample_games.pgn'

    def __init__(self, games=default_pgn):
        self.row = ['', '', 0, '', '']
        self.games = games
        self._conn = sqlite3.connect('lichess.db')
        self._cursor = self._conn.cursor()
        PGNs.generate_liches_db(self, self.games)
        self._conn.commit()
        self._conn.close()

    def generate_liches_db(self, games):
        """Method to read a lichess .pgn text file of games to a sqlite database.
        Args:
            games: plain text format of recorded chess games.
        """
        with open(games) as f:
            with tqdm.tqdm(total=os.path.getsize(games), unit_scale=0.00000001) as pbar:
                for line in f:
                    get_event(self, line)
                    get_date(self, line)
                    get_white_elo(self, line)
                    get_moves(self, line)
                    write_to_db(self, line, self.row[0], self.row[1], self.row[2], self.row[3], self.row[4])
                    pbar.update(len(line))


def wipe_db(self):
    self._cursor.execute('DELETE FROM lichess')


def get_event(self, line):
    if line[:6] == '[Event':
        self.row[4] = line.split('"')[1]


def get_date(self, line):
    # if line.startswith('[Date'):
    if line[:5] == '[Date':
        self.row[0] = line[7:-3:]


def get_white_elo(self, line):
    if line[:9] == '[WhiteElo':
        self.row[2] = line.split('"')[1]


def get_moves(self, line):
    line = line[0:80]
    if line[:1] == '1' or line[:2] == ' 0' or line[:2] == ' 1':
        full_line = line.split(' ')
        self.row[1] = str(add_moves(full_line))


def write_to_db(self, line, a, b, c, d, e):
    if line[:1] == '1' or line[:2] == ' 0' or line[:2] == ' 1':
        self._cursor.execute('INSERT INTO lichess VALUES(?,?,?,?,?)', (a, b, c, d, e))


def add_moves(moves):
    opening_moves = []
    # get first move
    try:
        opening_moves.append(moves[1])
    except IndexError:
        pass
    # get second move
    try:
        opening_moves.append(moves[6])
    except IndexError:
        pass    
    # get third move
    try:
        opening_moves.append(moves[12])
    except IndexError:
        pass
    return opening_moves

