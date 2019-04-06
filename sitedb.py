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



#pidTable.insert({'pid':'pid', 'id': 1})
#aidTable.insert({'aid':'aid', 'id': 1})

userTable.drop()
answerTable.drop()
questionTable.drop()
ipTable.drop()
pidTable.update_one({'pid':'pid'}, {"$set": {"id": 1 }} )
print('UPDATED DATA')
# limit = 25
# questFilter = []
# allQuestion = questionTable.find();


# for q in allQuestion:
#     if q['time'] <= 1553560844.375:
#         questFilter.append(q)
# print('THERE ARE ', len(questFilter))
# questFilter.sort(key=lambda x: x['time'], reverse=True)

# count = 0;
# for q in questFilter:
#     if(count == limit ):
#         break;
#     temp = {
#                 'id': str(q['pid']),
#                 'title':q['title'],
#                 'body': q['body'],
#                 'tags': q['tags'],
#                 'answer_count': 0,
#                 'media': None,
#                 'accepted_answer_id': None,
#                 'user':	{	
#                             'username': q['username'],
#                             'reputation': 0
#                         },
#                 'timestamp': q['time'],
#                 'score': 0,
#                 "view_count": q['view_count']
#             }
#     count= count +1
#     print(count, q)






userTable = db['user'] 
answerTable = db['answer']
questionTable = db['question']
ipTable = db['ip']
'''
use stack
db.createCollection("user")
db.createCollection("question")
db.createCollection("ip")
db.createCollection("answer")

'''

#userTable.remove()
#userTable.insert({'email': "kevin" , 'pass': None} )
#userTable.insert({'email': "nicole" , 'pass': None} )


#print( userTable.find_one({'email':'nicole'})['email']          )

#query = {"email": "mykey"}
#newVal = {"$set": {"key": "KKKK"}}  
#userTable.update_one(query, newVal)
