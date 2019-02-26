
var actualBoard = [' ',' ',' ',
				   ' ',' ',' ',
				   ' ',' ',' '];
var count = 0;
$(document).ready(function(){
	nextCell = 0;
	


	$('.cell').click(function(e){
		cellClicked = e.target.id;	
		var index = parseInt(cellClicked);
		

		if(actualBoard[index] != ' '){
			alert("Cell is taken. Please choose another cell.");
		}else{
			actualBoard[index] = 'X';
			markTheCell(actualBoard);
			
			$.ajax({
				url: '/ttt/play',
				contentType:"application/json",
	            dataType:"json",
				data: JSON.stringify({'grid' : actualBoard}),
				type: 'POST',
				success: function(resp){
					var grid = resp['grid'];// computers next move
					actualBoard = grid;
					//console.log("the grid is :" + grid);
					
					markTheCell(grid);

					var winner = resp['winner']
					if(spaceTaken(grid) == 0 && winner==' '){//if board is full, and the players are tie 
						markTheCell(grid);
						setTimeout(function() { 
							alert("Tie");
							clearBoard(); 
						}, 70);
					}
					if(winner == 'X'){ // HUman wins
						alert("Human Wins");
						clearBoard();
					}
					
					if(winner == 'O'){
						markTheCell(grid);
						setTimeout(function() { 
							alert("Computer Wins");
							clearBoard(); 
						}, 70);
						
					}
				},
				error: function(error){
					alert('Error in Ajax response');
				}
			});
		}	

	});

});

function spaceTaken(grid){
	var count= 0;
	for(var i = 0; i < grid.length; i++){
		if(grid[i] == ' '){
			count+=1;
		}
	}
	return count;

}
function clearBoard(){
	actualBoard = [' ',' ',' ',
				   ' ',' ',' ',
				   ' ',' ',' '];
	var cell = document.getElementsByClassName("cell");

	for(var i = 0; i < cell.length; i++){
		cell[i].innerHTML = "";
	}

}


function markTheCell(grid){
	for(var i = 0; i < grid.length; i++){
		$('#'+i.toString()).css({'font-size':'90px', 'text-align':'center' });
		if(grid[i] == 'X'){
			$('#'+i.toString()).text('X');
		}
		if(grid[i] == 'O'){
			$('#'+i.toString()).text('O');
		}
	}
}

// function markTheCell(cell, symbol){
// 	$('#'+cell.toString()).css({'font-size':'90px', 'text-align':'center' });
// 	$('#'+cell.toString()).text(symbol);
// 	actualBoard[parseInt(cell)]= symbol; 
// }

