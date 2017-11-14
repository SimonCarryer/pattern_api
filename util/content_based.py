import pandas as pd
from load_objects import load_compressed_pickled_object
from sklearn.metrics.pairwise import pairwise_distances
	
class ContentBasedRecommender:
	def __init__(self, pattern_names, transformed_features):
		self.pattern_names = list(pattern_names)
		self.features = transformed_features
		
	def get_closest_n(self, target, n=10):
		target_index = self.pattern_names.index(target)
		distances = pd.Series([i[0] for i in pairwise_distances(self.features, self.features[target_index])])
		closest = distances.argsort()[:n]
		return [self.pattern_names[i] for i in closest]
		
if __name__ == '__main__':
	features_url = 'https://s3.amazonaws.com/ravelry-data/features.pklz'
	print 'loading features'
	transformed_features = load_compressed_pickled_object(features_url)
	pattern_names_url = 'https://s3.amazonaws.com/ravelry-data/pattern_names.pklz'
	print 'loading patterns'
	pattern_names = load_compressed_pickled_object(pattern_names_url)
	rec = ContentBasedRecommender(pattern_names, transformed_features)
	print rec.get_closest_n('hitofude-cardigan', 10)