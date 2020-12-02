class PGN_DataFrame:
	"""PGN class to hold a dataframe object with a record of openings across
	a date range.
	"""
	def __init__(self, df):
		self.df = df

	def generate_total_games(self):
		"""Method to append a calculated column with the total number of games
			calculated by adding all numeric values in a row, ie. each date.
		Args:
			df: a Dataframe
		"""
		self.df['Total_Games'] = self.df[list(self.df.columns)].sum(axis=1)


	def sum_similar_moves(self, col, move_list):
		"""Append a calculated column that sums the values in columns whose name 
			belongs to a specified subset.
		Args:
			df: a DataFrame
			col: the name of the new column
			move_list: the naem of the columns from which to generate the
					   calculated column
		"""	
		self.df[col] = self.df[move_list].sum(axis=1)

	def generate_perc_played(self, col):
		"""Append a calculated column that displays the percentage of games that 
		   that have been played with the specified opening.
		Args:
			col: the name of the opening to analyze
		"""	
		new_col_name = col + '_%_played'
		self.df[new_col_name] = self.df[col]/self.df['Total_Games'] * 100