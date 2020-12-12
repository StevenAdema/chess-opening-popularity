import os
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime
from games import Games
from matplotlib.ticker import PercentFormatter
plt.style.use('fivethirtyeight')


def main():
    """Maps the popularity of an opening against the lichess.org database.
    Outputs the findings to a line graph.
    """
    cfg = get_configs()
    elo_range = '800-1000'
    opening_name = 'Queen\'s Gambit'
    opening = "['d4', 'd5', 'c4']"

    g = Games('/data/lichess.db', elo=elo_range, opening=opening)

    plot_popularity(g.df, opening_name, elo=elo_range)


def plot_popularity(df, opening_name, elo=None):
    """ Creates a line plot of the relative popularity of an opening over a defined
    period of time.
    Args:
        df: the DataFrame containing the date axis and column named 'opening' with
            the relative popularity of the move per each day
        opening_name: The plain text name of the opening for use in the legend
        elo: the elo range of the players using the opening for use in the legend
        """
    x = df['date'].tolist()
    x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
    x = [datetime.strftime(d, '%b-%d') for d in x]

    fig, ax = plt.subplots(figsize=(12, 6))
    # fig, ax = plt.subplots()
    plt.xticks(np.arange(0, 62, 7))
    ax.plot(x, df['opening_percentage_played'])
    plt.gca().yaxis.set_major_formatter(PercentFormatter(100, decimals=2))
    if elo is not None:
        plt.legend(labels=['% of games beginning with ' + opening_name + ' for ' + elo + ' ELO players'], loc=2)
    else:
        plt.legend(labels=['% of games beginning with ' + opening_name], loc=2)
    plt.title('Popularity of ' + opening_name + ' on lichess.org')
    plt.annotate("♕ Release of 'The Queen\'s Gambit'", (22.6, 1.73))
    plt.show()
    exit()


def get_configs():
    """Method to retrieve information from the configuration file.
    Returns:
        res: a dictionary with lists contained in config.yaml
    """
    dirname = os.path.dirname(__file__)
    conf = os.path.join(dirname, 'conf/config.yml')
    with open(conf) as f:
        res = yaml.safe_load(f)
    return res


if __name__ == '__main__':
    main()
