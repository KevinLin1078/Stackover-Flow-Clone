$(document).ready(function(){
                
   $("#logout").click( 
function(e) {
  $.ajax({
     url: '/logout',
     type: 'POST',
     contentType:"application/json",
     dataType:"json",
     data: JSON.stringify({}),
     success: function (data){
        
        window.location.href='/login'
     },
     error: function(err){
        alert("ERROR OCCURED WHILE ADDING USER " + err)
     }
  })
})
   
   $("#clickme").click( 
function(e) {
  $.ajax({
     url: '/search',
     type: 'POST',
     contentType:"application/json",
     dataType:"json",
     data: JSON.stringify({'q': $('#dev-table-filter').val() }),
     success: function (data){
               // data = JSON.parse(data)
               var myNode = document.getElementById("dev-table");
               var fc = myNode.children[1];
               while( fc ) {
                   myNode.removeChild( fc );
                   fc = myNode.firstChild;
               }
               var myvar = '<thead id=\'addHead\'> <tr> <th>    <a id=\'sortId\'>#</a></th> <th>    <a id=\'sortTitle\'>Questions</a>    </th> <th>    <a id=\'sortUser\'>User</a>  </th> <th>    <a id=\'sortDate\'>Date</a>         </th>  </tr></thead>';
               $( "#dev-table" ).append( myvar )
               myvar = '<tbody id=\'queryInfo\'></tbody>'
               $( "#dev-table" ).append( myvar )
               
               
               $.each(data['questions'],function(index,value){ 
                   
                   myvar = '<tr>'+
                           '            <th>' + value['id'] + '</th>'+
                           '            <th>' + '<a class="kevin" id="' + value['id'].toString() + '">'+ value['title'] + '</a>' + '</th>' +
                           '            <th>' + value['user']['username'] + '</th>'+
                           '            <th>' + value['timestamp'] + '</th>  '+
                           '        </tr>';
                   
                       $('#queryInfo').append(myvar)
                   
               });

     },
     error: function(err){
        alert("ERROR OCCURED WHILE PUTTING USER " + err)
     }
  })
})   
   $('#back_button').click(
       function(){
           $('#actual_body').hide()
           $('#dev-table').show()
           $('#searchMe').show()
       }
   )
   $("a.kevin").click( //clickes on question
   function() {
         var key = $(this).attr("id")
         alert(key)
         $.ajax({
            url: '/questions/' + key.toString(),
            type: 'GET',
            dataType:"html",
            success: function (data){
                        var data = JSON.parse(data);
                        $('#realQuestionID').text(key)
                        $('#question_title').text(data['question']['title'])
                        $('#question_body').text(data['question']['body'])
                        $('#actual_body').show()
                        $('#dev-table').hide()
                        $('#searchMe').hide()
                        
                        var myNode = document.getElementById("answerTable");
                        var fc = myNode.children[0];
                        while( fc ) {
                           myNode.removeChild( fc );
                           fc = myNode.firstChild;
                        }

                        $.each(data['answers'],function(index,value){ 
                           
                           myvar =  '<p style="border:1px solid green" class="input">' + value['answer'] + '</p><br>'
                              $('#answerTable').prepend(myvar)
                           
                        });
            },
            error: function(err){
               alert("ERROR OCCURED WHILE GETTING Question ID1 " + err)
            }
         })
})
   //answer_submit
   $("#answer_submit").click( //clickes on question
   function() {
      var body = $('#textarea').val()
       
      $.ajax({
         url: '/questions/' + $('#realQuestionID').text() + '/answers/add',
         type: 'POST',
               contentType:"application/json",
         dataType:"json",
         data: JSON.stringify({'body': body }),
         success: function (data){
                     stat = data['status'].toString()
                  
                     if(stat== "error"){
                        alert("Please Login to Answer Questions")
                     }else{
                        myvar = '<p class="input" style="border:1px solid green">' + body + '</p><br>'
                        $('#answerTable').prepend(myvar)
                        $('#textarea').val("")
                        alert("Answer Added")
                     }
         },
         error: function(err){
            alert("ERROR OCCURED WHILE PUTTING USER " + err)
         }
      })
})


   $(document).on( 'click', 'a.kevin',//clickes on question
function() {
       var key = $(this).attr("id")
       alert(key)
      $.ajax({
         url: '/questions/' + key.toString(),
         type: 'GET',
               dataType:"html",
         success: function (data){
                     var data = JSON.parse(data);
                     $('#realQuestionID').text(key)
                     $('#question_title').text(data['question']['title'])
                     $('#question_body').text(data['question']['body'])
                     $('#actual_body').show()
                     $('#dev-table').hide()
                     $('#searchMe').hide()
                     
                     var myNode = document.getElementById("answerTable");
                     var fc = myNode.children[0];
                     while( fc ) {
                        myNode.removeChild( fc );
                        fc = myNode.firstChild;
                     }
                     $.each(data['answers'],function(index,value){ 
                        myvar =  '<p class="input" style="border:1px solid green">' + value['answer'] + '</p><br>'
                           $('#answerTable').prepend(myvar)
                     });
         },
         error: function(err){
            alert("ERROR OCCURED WHILE PUTTING USER GETTING Question ID2" + err)
         }
      })
})

   $(document).on("contextmenu",function(){
   return false;
   }); 
   

   $(document).bind('keydown', function(e) {
       if(e.ctrlKey && (e.which == 80)) {
       e.preventDefault();
       return false;
       }
   });


   $(document).bind('keydown', function(e) {
       if(e.ctrlKey && (e.which == 83)) {
       e.preventDefault();
       return false;
       }
   });
   document.onkeydown = function(e) {
       if(event.keyCode == 123) {
       return false;
       }
       if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)){
       return false;
       }
       if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)){
       return false;
       }
       if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)){
       return false;
       }
   }


})