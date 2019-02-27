from flask import Flask
from routes import bp
import pymongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(bp)
app.config['CORS_HEADERS'] = 'Content-Type'

# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)


if __name__ == '__main__':
	app.debug=True
	app.run()


