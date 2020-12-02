import os
import pandas as pd
import yaml
import matplotlib.pyplot as plt
from PGN_DataFrame import PGN_DataFrame


def main():
	"""Maps the popularity of an opening against the Lichess database.
	Outputs the findings to a matplot line graph.
	"""
	# games = r'C:\Users\Steven\Documents\Projects\chess-analysis-master\game.pgn'
	# games = r'E:\pgns\lichess_db_standard_rated_2020-10.pgn'
	cfg = get_configs()
	openings_list = cfg['openings']
	openings_of_interest = aggregate_similar_moves("Queen's Gambit", openings_list)
	simple_name = 'Queens Gambit'
	# dates_list = cfg['dates']
	# # openings_dict = dict()
	# openings_dict = {ver: {col: 0 for col in openings_list} for ver in dates_list}

	# openings_dict = count_QBs(openings_dict, games)

	# df = pd.DataFrame.from_dict(openings_dict,orient='index')
	# df.to_csv(r'C:\Users\Steven\Documents\Projects\chess-analysis-master\games.csv', sep='|')
	df = pd.read_csv(r'C:\Users\Steven\Documents\Projects\chess-analysis-master\games.csv', sep='|')
	d = PGN_DataFrame(df)
	d.generate_total_games()
	d.sum_similar_moves(simple_name, openings_of_interest)
	d.generate_perc_played(simple_name)

	plot_popularity(d.df, simple_name)

def count_QBs(openings_dict, pgn):
	pgn_size = os.path.getsize(pgn)
	progress = 0
	with open(pgn, "r") as pgns:
		for line in pgns:
				progress = progress + len(line)
				if line.startswith('[Date'):
					current_date = line[7:-3:]
				if line.startswith('[Opening'):
					opening = line[10:-3:]
					try:
						openings_dict[current_date][opening] += 1
					except KeyError:
						openings_dict[current_date][opening] = 1
				if progress % 100000 == 0:
					progressPercent = (100*progress)/pgn_size
					print(progressPercent)
				# if progress % 10000000 == 0:
				# 	break

	return openings_dict


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


def aggregate_similar_moves(begins_with, openings_list):
	"""Create a list of similar openings by aggregating on openings that 
	   start with a similar set of characters.
	Args:
		begins_with: a string to group opening names
		openings_list: a list of openings from which to group
	Returns:
		most_list: a subset of openings_list containing openings of interest
	"""	
	move_list = [i for i in openings_list if i.startswith(begins_with)]
	return move_list


def plot_popularity(df, col_name):
	ax = plt.gca()
	y_name = col_name + '_%_played'
	df.plot(kind='line',x='Date',y=y_name,ax=ax)
	plt.show()

if __name__ == '__main__':
	main()
