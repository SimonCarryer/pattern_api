from flask import Flask, jsonify
from util.content_based import *
from util.collaborative import *

print 'loading patterns data'
#pattern_df = load_patterns('s3://ravelry-data/patterns_data.csv')

print 'transforming patterns data'
#pattern_features = transformed_features(pattern_df)

print 'loading user data'
#user_df = load_user_likes('s3://ravelry-data/user_data.csv')

print 'starting app'
app = Flask(__name__)
#app.config['content_rec'] = ContentBasedRecommender(pattern_df, pattern_features)
#app.config['collaborative_rec'] = CollaborativeRecommender(pattern_df, user_df)

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
    app.run()