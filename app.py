from flask import Flask, jsonify, request 
from textgenrnn import textgenrnn
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
	pass

#generates reviews for products
#paramters for this request are section and productID
@app.route("/reviewGen", methods=['GET'])
def reviewGen():
	section = json.loads(request.data)["section"]
	productID = json.loads(request.data)["id"]
	
	#checks if the section is in a valid category
	category = str(section).lower()
	if category == "steam":
		weights = "./models/steam/" + productID + ".hdf5"
	elif category == "yelp":
		weights = "./models/yelp/" + productID + ".hdf5"
	else:
		return jsonify("Bad request, please enter a valid section")
	
	#generates text
	textgen = textgenrnn(weights)	
	review = textgen.generate(return_as_list=True)

	return jsonify(review = review[0], fileUsed = weights)

#generates paragraph based on word given
@app.route("/contextGen", methods=['GET'])
def contextGen():
	keyword = json.loads(request.data)["keyword"]
	textgen = textgenrnn()
	output = textgen.generate(return_as_list=True, prefix = keyword)
	return jsonify(str(output[0]))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
