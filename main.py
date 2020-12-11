import os
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime
from matplotlib.ticker import PercentFormatter
plt.style.use('fivethirtyeight')


def main():
    """Maps the popularity of an opening against the lichess.org database.
    Outputs the findings to a line graph.
    """
    cfg = get_configs()
    conn = sqlite3.connect('/data/lichess_bak.db')
    cursor = conn.cursor()
    opening = "['e4', 'e5', 'Nf3']"
    opening_name = 'King\'s Knight'
    df = pd.read_sql_query('SELECT * from lichess_openings_summary WHERE Opening == (?)', conn, params=(opening,))
    conn.close()
    df['opening'] = 100*(df['openingCount'] / df['dailyGamesSum'])

    plot_popularity(df, opening_name)


def plot_popularity(df, opening_name):
    """ Creates a line plot of the relative popularity of an opening over a defined
    period of time.
    Args:
        df: the DataFrame containing the date axis and column named 'opening' with
            the relative popularity of the move per each day
        opening_name: The plain text name of the opening for use in the legend
        """
    x = df['date'].tolist()
    x = [datetime.strptime(d, '%Y.%m.%d') for d in x]
    x = [datetime.strftime(d, '%b-%d') for d in x]

    fig, ax = plt.subplots(figsize=(15, 7))
    plt.xticks(np.arange(0, 62, 7))
    ax.plot(x, df['opening'])
    plt.gca().yaxis.set_major_formatter(PercentFormatter(100, decimals=2))
    plt.legend(labels=['% of games beginning with ' + opening_name], loc=2)
    plt.title('Popularity of ' + opening_name + ' on lichess.org')
    plt.annotate("♕ Release of 'The Queen\'s Gambit'", (22.7, 3.915))
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
