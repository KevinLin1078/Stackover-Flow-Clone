import random

winTiles = [[1, 4, 7], [2, 5, 8], [3, 4, 5],
			[0, 1, 2], [6, 7, 8], [0, 4, 8], 
			[2, 4, 6], [0, 3, 6] ];

side = [0,2,6,8]


def getNextMove(board, start ):
	if(board[4] == ' ' and start == 1):				#If user didnt pick center, then server picks center
		board[4] = 'O'
		return [4, 'no']
	elif(board[4] != ' ' and start == 1):								#If user picks center, then server picks side

		available = []
		for s in side:
			if(board[s] == ' ' ):
				available.append(s)
		if len(available)!= 0 :
			mark = random.choice(available)
			board[mark] = 'O'
			return [mark, 'no']
	elif(start != 1):
		ret = checkWinningTile(board)
		if(ret != -1):
			board[ret] = 'O'
			return [ret, findWinner(board)[1]]
			
		ret2 = checkWinningTile2(board)
		if(ret2 != -1):
			board[ret2] = 'O'
			return [ret2, findWinner(board)[1]]

		


	for i in range (0, 9):
		if(board[i] == ' ' ):
			board[i] = 'O'
			return [i, findWinner(board)[1]]

	return [-1 , findWinner(board)[1]]

def pickCorner(board):
	available = []
	for s in side:
		if(board[s] == ' ' ):
			available.append(s)
	if(len(available)!= 0):
		mark = random.choice(available)
		board[mark] = 'O'
		return mark

def checkWinningTile(b): #b = board
	for win in winTiles:	

		if b[win[0]] == ' ' and b[win[1]] =='O' and b[win[2]] == 'O':
			return win[0]

		if b[win[0]] == 'O' and b[win[1]] ==' ' and b[win[2]] == 'O':
			return win[1]

		if b[win[0]] == 'O' and b[win[1]] =='O' and b[win[2]] == ' ':
			return win[2]
	return -1

def checkWinningTile2(b):
	for win in winTiles:
		if b[win[0]] == ' ' and b[win[1]] == 'X' and b[win[2]] == 'X':
			return win[0]

		if b[win[0]] == 'X' and b[win[1]] == ' ' and b[win[2]] =='X':
			return win[1]

		if b[win[0]] == 'X' and b[win[1]] =='X' and b[win[2]] == ' ':
			return win[2]

	return -1
def findWinner(b):
	for win in winTiles:
		if  b[win[0]] == b[win[1]] and b[win[0]] == b[win[2]] and b[win[0]] == 'X':
			return [True, 'X']

		if  b[win[0]] == b[win[1]] and b[win[0]] == b[win[2]] and b[win[0]] == 'O':
			return [True, 'O']
	return [False, ' ']
def countN(b):
	count = 0;
	for bs in b:
		if bs == ' ':
			count+=1
	return count
