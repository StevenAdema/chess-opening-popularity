import os
import pandas as pd
import yaml
import matplotlib.pyplot as plt
from PGN_DataFrame import PGN_DataFrame
from matplotlib.ticker import PercentFormatter
import matplotlib.dates as mdates


def main():
	"""Maps the popularity of an opening against the Lichess database.
	Outputs the findings to a matplot line graph.
	"""
	games = r'C:\Users\Steven\Documents\Projects\chess-analysis-master\data\game.pgn'
	# games = r'E:\nov_pgns\lichess_db_standard_rated_2020-11.pgn'
	cfg = get_configs()
	openings_list = cfg['openings']
	opening = ['d4','e5','c4']
	simple_name = 'Queens Gambit'
	dates_list = cfg['dates']
	openings_dict = {ver: {col: 0 for col in openings_list} for ver in dates_list}

	openings_dict = count_QBs(openings_dict, games, opening)

	df = pd.DataFrame.from_dict(openings_dict, orient='index')
	# df.to_csv(r'C:\Users\Steven\Documents\Projects\chess-analysis-master\data\games_nov.csv', sep='|') # save for quicker reruns
	df['Date'] = pd.to_datetime(pd.Series(df['Date']), format="%Y.%m.%d")
	d = PGN_DataFrame(df)
	d.generate_total_games()
	d.generate_perc_played(simple_name)
	d.split_pre_post_release('Queens Gambit_%_played')

	plot_popularity(d.df, simple_name)

def count_QBs(openings_dict, pgn, opening):
	pgn_size = os.path.getsize(pgn)
	progress = 0
	with open(pgn, "r") as pgns:
		for line in pgns:
				progress = progress + len(line)
				if line.startswith('[Date'):
					current_date = line[7:-3:]
				if line.startswith('1.'):
					try:
						first_move = line[3:5]
						second_move = line.split("2. ",1)[1][:2]
					except:
						continue
					if (first_move == opening[0]) and (second_move == opening[2]):
						openings_dict[current_date]['Queens Gambit'] += 1
					else:
						openings_dict[current_date]['Other'] += 1
				if progress % 1000000 == 0:
					progressPercent = (100*progress)/pgn_size
					print(progressPercent)

	return openings_dict


def plot_popularity(df, col_name):
	"""Plot the result
	"""
	df = df.set_index('Date')
	x_list = df.index.values
	print(x_list)
	# df = df[['Other','Queens Gambit']]
	color_map = ['#67B3E0', '#2274A5']
	print(df['Queens Gambit_%_played pre release'])
	plt.stackplot(x_list, df['Queens Gambit_%_played pre release'],  df['Queens Gambit_%_played post release'], colors = color_map)
	plt.legend(loc='upper left')
	plt.margins(0,0)
	plt.ylim(8.5, 9.5)
	plt.axhline(y=9.06, color='#39A3E0', ls='--', xmax=0.38, linewidth=2)
	plt.axhline(y=9.2, color='#0967A0', ls='--', xmin=0.38, linewidth=2)
	plt.gca().yaxis.set_major_formatter(PercentFormatter(100, decimals=1))
	dtFmt = mdates.DateFormatter('%d-%b')
	plt.gca().xaxis.set_major_formatter(dtFmt)
	plt.legend(labels=['pre-release avg.', 'post-release avg.'], loc=2)
	plt.title('The Queen\'s Gambit Opening Popularity')
	plt.annotate("Release of Netflix series", ('2020-10-24',8.8))
	plt.show()


def get_configs():
	"""Method to retriece information from the configuration file.
	Returns:
		res: a dictionary with lists containined in config.yaml
	"""
	dirname = os.path.dirname(__file__)
	conf = os.path.join(dirname, 'conf/config.yml')
	with open(conf) as f:
		res = yaml.safe_load(f)
	return res



if __name__ == '__main__':
	main()
