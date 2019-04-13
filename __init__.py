from flask import Flask
from routes import bp, app
import pymongo
from flask_cors import CORS


CORS(app)
app.register_blueprint(bp)
app.config['CORS_HEADERS'] = 'Content-Type'



if __name__ == '__main__':
	app.run()


