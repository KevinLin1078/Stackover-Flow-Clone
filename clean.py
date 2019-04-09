from flask import Flask 
import pymongo 
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client['stack']         #    use wp2

userTable = db['user'] 
answerTable = db['answer']
aidTable = db['answer_id']
questionTable = db['question']
pidTable = db['pid']
ipTable = db['ip']
questionIndex = db['questionIndex']
answerIndex = db['answerIndex']


userTable.drop()
answerTable.drop()
answerTable.drop()
questionTable.drop()
pidTable.drop()
ipTable.drop()
questionIndex.drop() 
answerIndex.drop()

userTable = db['user'] 
answerTable = db['answer']
questionTable = db['question']
ipTable = db['ip']
questionIndex = db['questionIndex']
answerIndex = db['answerIndex']
aidTable = db['answer_id']
pidTable = db['pid']

userTable.insert({})
answerTable.insert({})
questionTable.insert({})
ipTable.insert({})
questionIndex.insert({})
answerIndex.insert({})
pidTable.insert({'pid':'pid', 'id': 1})
aidTable.insert({'aid':'aid', 'id': 1})

userTable.delete_many({})
answerTable.delete_many({})
questionTable.delete_many({})
ipTable.delete_many({})
questionIndex.delete_many({})
answerIndex.delete_many({})


# def rank(body):
# 	b = body
# 	body = str(body).split()
# 	diction = {}
# 	print("ranking body .... ", body)
# 	for word in body:
# 		word = word.encode("utf-8")
# 		print("word is : ", word)
# 		arr = questionIndex.find_one({word:word})
# 		if arr != None:
# 			arr = arr['arr']
# 			for item in arr:
# 				key = str(item[0]).encode("utf-8")
# 				if key not in diction:
# 					diction[key] = 1
# 				else:
# 					diction[key] +=1
# 	import operator
# 	sorted_d = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)  
# 	return sorted_d

# print(rank('logging branches'))

print('UPDATED DATA')



# print("WITH QUERY")
# search_query = {}
# search_query['$or'] = []

# query_title = {}
# query_title['$or'] = []

# query_body = {}
# query_body['$or'] =[]

# query = query.split(' ')

# for each in query:
#    term = {}
#    term['$or'] = []
#    term['$or'].append({'title':{'$regex': ' ' + each}})
#    term['$or'].append({'title':{'$regex': each + ' '}})
#    query_title['$or'].append(term)

#    term = {}
#    term['$or'] = []
#    term['$or'].append({'body':{'$regex': ' ' + each}})
#    term['$or'].append({'body':{'$regex': each + ' '}})
#    query_body['$or'].append(term)

# search_query['$or'].append(query_title)
# search_query['$or'].append(query_body)
