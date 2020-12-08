import pandas as pd
import numpy as np

np.set_printoptions(linewidth=500)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 50)

class PGNs:
    """PGN class to hold a dataframe object with a record of openings across
    a date range.
    """
    games = r'C:\Users\Steven\Documents\Projects\chess-analysis-master\data\game.pgn'
    cols = ['Date','Opening','WhiteELO','TimeControl','Event']
    df = pd.DataFrame(columns=cols)
    is_new_game = False
    i = 0

    def __init__(self):
        self.df = pd.DataFrame(columns=self.cols)
        PGNs.add_pgn(self, self.games)
        print(self.df)
        self.df.to_csv(r'C:\Users\Steven\Documents\Projects\chess-analysis-master\games.csv', sep='|', index=False)

    def add_pgn(self, games):
        """Method to append a calculated column with the total number of games
            calculated by adding all numeric values in a row, ie. each date.
        Args:
            df: a Dataframe
        """
        with open(games) as infile:
            for line in infile:
                check_event(self, self.cols, self.i, line)
                check_date(self, self.i, line)
                check_white_elo(self, self.i, line)
                check_moves(self, self.i, line)


def check_event(self, c, i, line):
    if line.startswith('[Event'):
        event = line.split('"')[1]
        new_row = pd.Series({c[0]: '', c[1]: '', c[2]: 0, c[3]: '', c[4]: event })
        self.df = self.df.append(new_row, ignore_index=True)


def check_date(self, i, line):
    if line.startswith('[Date'):
        date = line[7:-3:]
        self.df['Date'][i] = date


def check_moves(self, i, line):
    if line.startswith('1') or line.startswith(' 0') or line.startswith(' 1'):
        full_line = line.split(' ')
        moves = add_moves(full_line)
        self.df['Opening'][i] = moves
        self.i = self.i + 1


def check_white_elo(self, i, line):
    if line.startswith('[WhiteElo'):
        elo = line.split('"')[1]
        self.df['WhiteELO'][i] = elo


def add_moves(moves):
    opening_moves = []
    # get first move
    try:
        opening_moves.append(moves[1])
    except:
        pass
    # get second move
    try:
        opening_moves.append(moves[6])
    except:
        pass    
    #get third move
    try:
        opening_moves.append(moves[12])
    except:
        pass
    return opening_moves


p = PGNs()

