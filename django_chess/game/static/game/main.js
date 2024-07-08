dic_pieces = {
    '-1' : '<i class="fa-regular fa-chess-pawn"></i>',
    '-2' : '<i class="fa-regular fa-chess-rook"></i>',
    '-3' : '<i class="fa-regular fa-chess-knight"></i>',
    '-4' : '<i class="fa-regular fa-chess-bishop"></i>',
    '-5' : '<i class="fa-regular fa-chess-queen"></i>',
    '-6' : '<i class="fa-regular fa-chess-king"></i>',
     '1' : '<i class="fa-solid fa-chess-pawn"></i>',
     '2' : '<i class="fa-solid fa-chess-rook"></i>',
     '3' : '<i class="fa-solid fa-chess-knight"></i>',
     '4' : '<i class="fa-solid fa-chess-bishop"></i>',
     '5' : '<i class="fa-solid fa-chess-queen"></i>',
     '6' : '<i class="fa-solid fa-chess-king"></i>',
     '' : ''
}





$(document).ready(function() {
    $('button').click(function() {

        // Define a variable to store the result
        var request_response;
        const chessboard = document.getElementById("chessboard");
        board = chessboard.getAttribute("data-chessboard");
        console.log(board)

        const csrftoken = document.getElementById('csrf').getAttribute('data-csrf');
        console.log(csrftoken)

       // Set up default AJAX settings
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

// Your AJAX call
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/test/",
    contentType: "application/json",
    data: JSON.stringify({
        'board': board
    }),
    success: function(data) {
        // Store the result in the variable
        var request_response = data;

        // Log the result to the console
        console.log("Result from AJAX:", request_response);

        // Update the DOM to display the result
        $('#ajax-response').text(data.message);
    },
    error: function(jqXHR, textStatus, errorThrown) {
        // Handle errors if needed
        console.error('Error: ' + textStatus + ' - ' + errorThrown);

        // Update the DOM with the error message if necessary
        $('#ajax-response').text('Error: ' + textStatus + ' - ' + errorThrown);
    }
});


        //testing piecen update in js

        // Step 2: Get the <div> element where you want to render the HTML
        const divElement = document.getElementById('0');
        if (divElement) {
            //just checkoing if i can search the dic for the html
            const htmlString = dic_pieces['1'];
            divElement.innerHTML = htmlString;
        } else {
            console.error('Element with class "piece" and id "0" not found.');
        }


        // Note: ajaxResult here will be undefined because $.ajax is asynchronous
        // If you need to use ajaxResult outside of $.ajax, consider async handling
        // or pass it to another function inside success callback.
    });
});
