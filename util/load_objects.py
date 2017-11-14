import urllib
import StringIO
import gzip
import cPickle as pickle

def load_compressed_pickled_object(file_url):
	opener = urllib.URLopener()
	myfile = opener.open(file_url)
	compressed_string = myfile.read()
	compressedFile = StringIO.StringIO(compressed_string)
	decompressedFile = gzip.GzipFile(fileobj=compressedFile)
	loaded_object = pickle.load(decompressedFile)
	return loaded_object
	
	
if __name__ == '__main__':
	url = "https://s3.amazonaws.com/ravelry-data/pattern_names.pklz"
	loaded_object = load_compressed_pickled_object(url)
	print len(loaded_object)