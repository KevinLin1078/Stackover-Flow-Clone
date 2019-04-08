
def question(title, body, pid):
   title = str(title).split()
   body = str(body).split()
   if len(title) == 0:
      for word in title:
         result = questionIndex.find_one({'term': word})
         if result == None:
            questionIndex.insert({ 'term': word, 'arr': {pid: 1} )
         else:
            temp = result['arr']
            temp[pid] +=1
            questionIndex.update_one({'term':word}, {'$set': {'arr': temp[pid]}}  )

   if len(body) != 0:
      for word in title:
         result = questionIndex.find_one({'term': word})
         if result == None:
            questionIndex.insert({ 'term': word, 'arr': [pid]})
         else:
            temp = result['arr']
            temp[pid] +=1
            questionIndex.update_one({'term':word}, {'$push': {'arr': temp[pid]}}  )