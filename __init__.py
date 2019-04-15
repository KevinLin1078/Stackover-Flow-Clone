    
from flask import Flask
import pymongo
from flask_cors import CORS
from routes import bp, app

CORS(app)
app.register_blueprint(bp)
app.config['CORS_HEADERS'] = 'Content-Type'



if __name__ == '__main__':
	app.run()