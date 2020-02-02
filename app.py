from flask import Flask, jsonify, request 
from textgenrnn import textgenrnn

from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import string
import pandas as pd
import numpy as np
import keras
import sklearn
import pickle
import json

app = Flask(__name__)

#test api
@app.route("/")
def hello():
	return "hello world"

#classifies steam reviews
@app.route("/classifySteam", methods=['GET'])
def classifySteam():
	pass

#classifies yelp reviews
@app.route("/classifyYelp", methods=['GET'])
def classifyYelp():
	text = json.loads(request.data)["review"]
	with open('./models/Predict/tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)

	sequences = tokenizer.texts_to_sequences([text])
	data = pad_sequences(sequences, maxlen=500)

	new_model = keras.models.load_model('./models/Predict/fakeYelp.h5')
	result = new_model.predict_proba(np.array(data))

	if result[0][0] < 0.5:
		prediction = 0
	else:
		prediction = 1

	return jsonify(str(prediction))

#generates reviews for products
#paramters for this request are section and productID
@app.route("/reviewGen", methods=['GET'])
def reviewGen():
	section = json.loads(request.data)["section"]
	productID = json.loads(request.data)["id"]
	
	#checks if the section is in a valid category
	weights = file_search(section,productID)
	
	#generates text
	textgen = textgenrnn(weights)	
	review = textgen.generate(return_as_list=True)

	return jsonify(review = review[0], fileUsed = weights)


#Gives the negative and positive aspects about a product 
@app.route("/featureYelp", methods=['GET'])
def features_extraction():
	#review_type = json.loads(request.data)["type"]
	#businessID = json.loads(request.data)["id"]
	pass
	

#generates paragraph based on word given
@app.route("/contextGen", methods=['GET'])
def contextGen():
	section = json.loads(request.data)["section"]
	productID = json.loads(request.data)["id"]
	keyword = json.loads(request.data)["keyword"]
	weights = file_search(section,productID)


	textgen = textgenrnn(weights)
	output = textgen.generate(return_as_list=True, prefix = keyword)
	return jsonify(str(output[0]))


#search for files
def file_search(section, productID):
	category = str(section).lower()
	if category == "steam":
		weights = "./models/steam/" + productID + ".hdf5"
	elif category == "yelp":
		weights = "./models/yelp/" + productID + ".hdf5"
	
	return weights


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
