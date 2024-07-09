var updated_board;
let moves = [];



function SendBoardMove() {
    return new Promise((resolve, reject) => {

    // Define a variable to store the result
    var request_response;
    //in case there was a board update it picks from last update
    if (updated_board){
        console.log('UPDATED BOARD WORKED')
        board = updated_board
    } else{
        const chessboard = document.getElementById("chessboard");
        board = chessboard.getAttribute("data-chessboard");
    }

    const csrftoken = document.getElementById('csrf').getAttribute('data-csrf');

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
            'board': board,
            'moves': moves
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


//Saves piece index thatplayer wants to move
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