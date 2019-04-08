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





def questionStore(title, body, pid):
   parseAlgo(title, pid)
   parseAlgo(body, pid)



def parseAlgo(body, pid):
   body = str(body).split()
   if len(body) != 0:
      for word in body:
         result = questionIndex.find_one({word: word})
         if result == None:
            questionIndex.insert({ word: word, 'arr': [[pid,1]]  })
         else:
            arr = result['arr']
            found = False
            for i in range(0, len(arr)):
               if arr[i][0] == pid:
                  arr[i][1]+=1
                  found = True
                  break
            if found == True:      
               questionIndex.update_one({word:word}, {'$set': {'arr': arr  }}  )
            else:
               questionIndex.update_one({word:word}, {'$push': {'arr': [pid, 1]  }}  )

def rank(body):
   b = body
   body = str(body).split()
   diction = {}

   for word in body:
      arr = questionIndex.find_one({word:word})['arr']
      for item in arr:
         key = str(item[0])
         if key not in diction:
            diction[key] = 1
         else:
            diction[key] +=1
   print(diction)
   import operator
   sorted_d = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)  
   print(sorted_d)
   return sorted_d

#2 1 3

questionStore('question one', 'this is a hello world', 11)
questionStore('question two', 'hello world', 22)
questionStore('question two', 'final hello to the', 33)

rank('hello world')




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


# def question(title, body, pid):
#    title = str(title).split()
#    body = str(body).split()
   
#    if len(title) != 0:
#       for word in title:
#          result = questionIndex.find_one({word: word})
#          if result == None:
#             questionIndex.insert({ word: word, 'arr': [[pid, 1]] } )
#          else:
#             temp = result['arr']
#             for i in range(0, len(temp)):
#                if temp[i][0] == pid:
#                   temp[i][1] +=1
#                   break;

#             questionIndex.update_one({word:word}, {'$set': {'arr': temp  }}  )

#    if len(body) != 0:
#       for word in body:
#          result = questionIndex.find_one({word: word})
#          if result == None:
#             questionIndex.insert({ word: word, 'arr': [[pid, 1]] } )
#          else:
#             temp = result['arr']
#             for i in range(0, len(temp)):
#                if temp[i][0] == pid:
#                   temp[i][1] +=1
#                   break;
#             questionIndex.update_one({word:word}, {'$set': {'arr': temp  }}  )