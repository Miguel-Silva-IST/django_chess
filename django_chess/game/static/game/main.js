// Use csrfToken for your AJAX requests

//const csrftoken = getCookie('csrftoken');
//console.log(csrftoken)


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


        // Note: ajaxResult here will be undefined because $.ajax is asynchronous
        // If you need to use ajaxResult outside of $.ajax, consider async handling
        // or pass it to another function inside success callback.
    });
});
