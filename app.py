from flask import Flask, jsonify, request 
import json

app = Flask(__name__)

#test api
@app.route("/")
def hello():
	return "hello world"

#classifies steam reviews
@app.route("/classifySteam")
def classifySteam():
	test = json.loads(request.data)["input"]
	output = "hello" + str(test)
	return jsonify(output)

#classifies yelp reviews
@app.route("/classifyYelp")
def classifyYelp():
	pass

#generates reviews for products
@app.route("/reviewGen")
def reviewGen():
	pass

#generates paragraph based on word given
@app.route("/contextGen")
def contextGen():
	pass

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
