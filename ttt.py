from flask import Flask, render_template, request, url_for, json, redirect, Blueprint
import datetime
import tictac
blue = Blueprint('ttt', __name__, template_folder='templates', url_prefix='/ttt')



@blue.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@blue.route('/ttt/play/', methods=['GET', 'POST'])
def play():
	name = request.form['name']
	date =  datetime.date.today()
	return render_template('tic.html', name=name, date=date)


@blue.route('/cellInfo', methods=['GET', 'POST'])
def cellInfo():
	jsonReceived = request.json	
	board = jsonReceived['board'] # Array view of the board
	print("adsfjkl")
	#tictac.getNextMove(board)
	return json.dumps({'status':'Yah!! AJAX worsk. Meow', 'nextMove':0})