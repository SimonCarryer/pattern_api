from flask import Flask, jsonify
from util.load_objects import load_compressed_pickled_object
from util.content_based import ContentBasedRecommender
from util.collaborative import CollaborativeRecommender

pattern_names_url = 'https://s3.amazonaws.com/ravelry-data/pattern_names.pklz'
print 'loading patterns'
pattern_names = load_compressed_pickled_object(pattern_names_url)

product_list_url = 'https://s3.amazonaws.com/ravelry-data/product_list.pklz'
print 'loading products'
product_list = load_compressed_pickled_object(product_list_url)

user_matrix_url = 'https://s3.amazonaws.com/ravelry-data/user_matrix.pklz'
print 'loading user matrix'
user_matrix = load_compressed_pickled_object(user_matrix_url)

features_url = 'https://s3.amazonaws.com/ravelry-data/features.pklz'
print 'loading features'
transformed_features = load_compressed_pickled_object(features_url)

print 'starting app'
app = Flask(__name__)
app.config['content_rec'] = ContentBasedRecommender(pattern_names, transformed_features)
app.config['collaborative_rec'] = CollaborativeRecommender(user_matrix, pattern_names, product_list)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/content_based/<string:pattern_name>')
def content_based(pattern_name):
	try:
		return jsonify(app.config['content_rec'].get_closest_n(pattern_name))
	except:
		return jsonify(["Doesn't look like we found anything"])

@app.route('/collaborative/<string:pattern_name>')
def collaborative(pattern_name):
	try:
		return jsonify(app.config['collaborative_rec'].get_closest_n(pattern_name))
	except:
		return jsonify(["Doesn't look like we found anything"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)