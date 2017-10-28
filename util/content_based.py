import pandas as pd
from constants import required, fillna_dict
from transform_objects import transform_set, weights
from feature_engineers import *
from copy import deepcopy
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.pipeline import FeatureUnion, Pipeline

def load_patterns(filepath):
	df = pd.read_csv(filepath)
	df = df.dropna(subset=required)
	df = df.fillna(fillna_dict)
	return df
	
def transformed_features(df):
	fu = FeatureUnion(transform_set, transformer_weights=weights)
	fu.fit(df)
	return fu.transform(df)
	
class ContentBasedRecommender:
	def __init__(self, df, transformed_features):
		self.pattern_names = list(df.permalink)
		self.features = transformed_features
		
	def get_closest_n(self, target, n=10):
		target_index = self.pattern_names.index(target)
		distances = pd.Series([i[0] for i in pairwise_distances(self.features, self.features[target_index])])
		closest = distances.argsort()[:n]
		return [self.pattern_names[i] for i in closest]
		
if __name__ == '__main__':
	data_path = 's3://ravelry-data/patterns_data.csv'
	df = load_patterns(data_path)
	features = transformed_features(df)
	rec = ContentBasedRecommender(df, features)
	print rec.get_closest_n('hitofude-cardigan', 10)