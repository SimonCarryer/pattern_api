import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from load_objects import load_compressed_pickled_object
	
class CollaborativeRecommender:
	def __init__(self, user_matrix, pattern_names, product_list):
		self.matrix = user_matrix
		self.product_list = product_list
		self.pattern_names = pattern_names
		
	def get_closest_n(self, target_name, number=10):
		pattern_id = self.pattern_names[self.pattern_names == target_name].index[0]
		target = self.product_list.index(pattern_id)
		distances = pd.Series([i[0] for i in pairwise_distances(self.matrix, self.matrix[target], metric='euclidean')]).argsort().values
		similars = [self.product_list[n] for n in distances[:number]]
		return [self.pattern_names[i] for i in similars]

if __name__ == '__main__':
	
	pattern_names_url = 'https://s3.amazonaws.com/ravelry-data/pattern_names.pklz'
	print 'loading patterns'
	pattern_names = load_compressed_pickled_object(pattern_names_url)
	
	product_list_url = 'https://s3.amazonaws.com/ravelry-data/product_list.pklz'
	print 'loading products'
	product_list = load_compressed_pickled_object(product_list_url)

	user_matrix_url = 'https://s3.amazonaws.com/ravelry-data/user_matrix.pklz'
	print 'loading user matrix'
	user_matrix = load_compressed_pickled_object(user_matrix_url)

	rec = CollaborativeRecommender(user_matrix, pattern_names, product_list)
	print rec.get_closest_n('cry-of-the-direwolf')