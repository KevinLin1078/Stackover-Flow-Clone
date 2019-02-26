from flask import Flask
from routes import bp
import pymongo
#WHATS FOOD
app = Flask(__name__)
app.register_blueprint(bp)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)
print("mongo")

if __name__ == '__main__':
	app.debug=True
	app.run()


