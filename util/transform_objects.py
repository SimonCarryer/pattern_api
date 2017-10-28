from feature_engineers import *
from copy import deepcopy
from sklearn.pipeline import FeatureUnion, Pipeline


transformers = {
	'bag of words': NameGettingPipeline([('vectoriser', CountVectorizer(min_df=0.002, max_df=0.2, stop_words='english')), 
							  ('weighting', TfidfTransformer())
										]),
	'keyword list': NameGettingPipeline([('vectoriser', CountVectorizer(tokenizer=lambda x: x.split('|'))), 
							  ('weighting', TfidfTransformer())]),
	'minmax': MinMaxWrapper(),
	'one-hot': OneHotWrapper()
}

data_transform = [
	('keywords', 'keyword list', 1),
	('category', 'keyword list', 2),
	('difficulty', 'minmax', 2),
	('ply', 'minmax', 3),
	('gauge', 'minmax', 1),
	('yardage', 'minmax', 1),
	('craft', 'one-hot', 4),
	('gauge_pattern', 'bag of words', 1)  
]

transform_set = [(column, NameGettingPipeline([(
					'selector', ItemSelector(column)), 
				('transformer', deepcopy(transformers[transform_type]))
				])) for column, transform_type, weight in data_transform]
				
weights = {column: weight for column, transform_type, weight in data_transform}