import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from math import log, sqrt
from content_based import load_patterns
from scipy.sparse import csr_matrix


def load_user_likes(filepath):
	return pd.read_csv(filepath)
	
	
class CollaborativeRecommender:
	def __init__(self, patterns_df, user_likes):
		self.matrix, self.pattern_ids = self.make_matrix(user_likes)
		patterns_df.index = patterns_df['permalink']
		self.pattern_id_lookup = patterns_df['pattern_id'].to_dict()
		patterns_df.index = patterns_df['pattern_id']
		self.pattern_name_lookup = patterns_df['permalink'].to_dict()
		
	
	def make_matrix(self, df):
		users = list(df.user_id.unique())
		products = list(df.pattern_id.unique())
		data = np.ones(len(df))
		col = df.user_id.astype('category', categories=users).cat.codes
		row = df.pattern_id.astype('category', categories=products).cat.codes
		N = len(users)
		idf = [1. + log(N / (1. + p)) for p in df.groupby('user_id').size()]
		weighted = [sqrt(hits) * idf[userid] for hits, userid in zip(data, col)]
		return csr_matrix((weighted, (row, col)), shape=(len(products), len(users))), products
		
	def get_closest_n(self, target_name, number=10):
		pattern_id = self.pattern_id_lookup[target_name]
		target = self.pattern_ids.index(pattern_id)
		distances = pd.Series([i[0] for i in pairwise_distances(self.matrix, self.matrix[target], metric='euclidean')]).argsort().values
		similars = [self.pattern_ids[n] for n in distances[:number]]
		return [self.pattern_name_lookup[i] for i in similars]

if __name__ == '__main__':
	data_path = 's3://ravelry-data/patterns_data.csv'
	patterns_df = load_patterns(data_path)
	data_path = '../../../../think_data/user_data.csv'
	user_df = load_user_likes(data_path)
	rec = CollaborativeRecommender(patterns_df, user_df)
	print rec.get_closest_n('cry-of-the-direwolf')