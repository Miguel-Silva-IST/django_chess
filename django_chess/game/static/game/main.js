var updated_board;
let moves = [];
var play_id = 0;



function SendBoardMove() {
    return new Promise((resolve, reject) => {

    //in case there was a board update it picks from last update
    if (updated_board){
        console.log('Getting board from JS variable')
        board = updated_board
    } else{
        console.log('Getting board from template variable')
        const chessboard = document.getElementById("chessboard");
        board = chessboard.getAttribute("data-chessboard");
    }

    const csrftoken = document.getElementById('csrf').getAttribute('data-csrf');
    const suk_player = document.getElementById('suk_player').getAttribute('data-suk_player');

    // Set up default AJAX settings
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    //AJAX call
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/move/",
        contentType: "application/json",
        data: JSON.stringify({
            'moves': moves,
            'suk_player': suk_player
        }),
        success: function(data) {
            //returns promise
            resolve(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle errors if needed
            console.error('Error: ' + textStatus + ' - ' + errorThrown);
        }
    });
})
};



function EndGame() {
    return new Promise((resolve, reject) => {
        
    const csrftoken = document.getElementById('csrf').getAttribute('data-csrf');
    const suk_player = document.getElementById('suk_player').getAttribute('data-suk_player');

    // Set up default AJAX settings
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    //AJAX call
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/end_game/",
        contentType: "application/json",
        data: JSON.stringify({
            'end_game': 1,
            'suk_player': suk_player
        }),
        success: function(data) {
            //returns promise
            resolve(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle errors if needed
            console.error('Error: ' + textStatus + ' - ' + errorThrown);
        }
    });
})
};



//Saves piece index that player wants to move
function move_track(moves, piece_index){
    console.log(piece_index)
    if (moves.length == 0) {
        moves.push(piece_index)
        console.log(moves)
        return 0
    }
    else if (moves.length == 1){
        if (moves[0].toString() == piece_index.toString()){
            console.log(moves[0].toString(), '==',piece_index.toString())
            moves.pop()
            console.log('First move was removed')
            return 0
        } else{
            moves.push(piece_index)
            console.log(moves)
            console.log('Submiting piece_index:',moves, 'to the endpoint /moves/')
            SendBoardMove().then(function(result) {
                if (result.move){
                    updated_board = result.updated_board
                    console.log('There was a move!')
                    render_updated_board()
                } else{
                    console.log('Impossible move!')
                    moves.pop()
                    moves.pop()
                }
                
            }).catch(function(error) {
                console.error('Error:', error);
            });
            return 0

        } 
    }
};


function render_updated_board(){
    console.log('MOVES---->',moves)
    square_i = document.getElementById(moves[0])
    square_f = document.getElementById(moves[1])
    square_f.innerHTML = square_i.innerHTML 
    square_i.innerHTML = ''
    moves.pop()
    moves.pop()
}


document.addEventListener('DOMContentLoaded', (event) => {
    const endGameButton = document.getElementById('end_game_button');
    const endGamePopup = document.getElementById('end_game_popup');
    const closePopupButton = document.getElementById('close_end_game_popup');
  
    endGameButton.addEventListener('click', () => {
      endGamePopup.style.display = 'block';
    });
  
    closePopupButton.addEventListener('click', () => {
      endGamePopup.style.display = 'none';
    });
  });
  



  function GetTimeTravell() {
    // Sends a get request and receives indexed_board
    // After receiving indexed_board it calls the render 

    return new Promise((resolve, reject) => {

    const csrftoken = document.getElementById('csrf').getAttribute('data-csrf');
    const suk_player = document.getElementById('suk_player').getAttribute('data-suk_player');

    // Set up default AJAX settings
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    //AJAX call
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/time_travell/",
        contentType: "application/json",
        data: JSON.stringify({
            'play_id': play_id,
            'suk_player': suk_player
        }),
        success: function(data) {
            //returns promise
            resolve(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle errors if needed
            console.error('Error: ' + textStatus + ' - ' + errorThrown);
        }
    });
})
};




function TimeTravell(travell_direction) {
    //runs through full board and modifies inner html
    if (travell_direction == 'previous'){
        play_id++
    } else if (travell_direction == 'next') {
        play_id--
    }

    console.log('Showing play_id',play_id)

    GetTimeTravell().then(function(result) {
        if (result.indexed_chessboard){
            console.log(result.indexed_chessboard)
            console.log(result.dic_pieces)
            render_full_board(result.indexed_chessboard, result.dic_pieces)
        } else{
            console.log('Couldnt receive time travell board state!!')
            //removes play_id increment/decrement to avoid acumulation
            if (travell_direction == 'previous'){
                play_id--
            } else if (travell_direction == 'next') {
                play_id++
            }
        }
        
    }).catch(function(error) {
        console.error('Error:', error);
    });
    return 0
}



function render_full_board(indexed_chessboard, dic_pieces){
    
    for (let row = 0; row < indexed_chessboard.length; row++) {
        for (let col = 0; col < indexed_chessboard[row].length; col++) {
            // Access the first and second elements of each pair
            let piece = indexed_chessboard[row][col][0];
            let index = indexed_chessboard[row][col][1];
            square = document.getElementById(index)
            piece_html = dic_pieces[piece]
            square.innerHTML = piece_html
        }
    }
}