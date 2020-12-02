import os
import pandas as pd
import yaml


def main():
    # games = r'C:\Users\Steven\Documents\Projects\chess-analysis-master\game.pgn'
    # games = r'E:\pgns\lichess_db_standard_rated_2020-10.pgn'
    cfg = get_configs()
    openings_list = cfg['openings']
    queens_list = [i for i in openings_list if i.startswith("Queen's Gambit")]
    print(queens_list)

    # dates_list = cfg['dates']
    # # openings_dict = dict()
    # openings_dict = {ver: {col: 0 for col in openings_list} for ver in dates_list}

    # openings_dict = count_QBs(openings_dict, games)

    # df = pd.DataFrame.from_dict(openings_dict,orient='index')
    # df.to_csv(r'C:\Users\Steven\Documents\Projects\chess-analysis-master\games.csv', sep='|')
    df = pd.read_csv(r'C:\Users\Steven\Documents\Projects\chess-analysis-master\games.csv', sep='|')
    df['Total_Games'] = df[list(df.columns)].sum(axis=1)
    df['Queens_Gambit'] = df[queens_list].sum(axis=1)
    df['Percentage_QB_Played'] = df['Queens_Gambit']/df['Total_Games'] * 100
    print(df['Percentage_QB_Played'])

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
	dirname = os.path.dirname(__file__)
	conf = os.path.join(dirname, 'conf/config.yml')
	with open(conf) as f:
		res = yaml.safe_load(f)
	return res


if __name__ == '__main__':
    main()
