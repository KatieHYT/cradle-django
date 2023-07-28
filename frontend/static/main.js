
$(document).ready(function() {
    // Send the form on enter keypress and avoid if shift is pressed
    $('#prompt').keypress(function(event) {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            $('form').submit();
        }
    });
    $('form').on('submit', function(event) {
        event.preventDefault();
    // get the CSRF token from the cookie
    var csrftoken = Cookies.get('csrftoken');
    
    // set the CSRF token in the AJAX headers
    $.ajaxSetup({
        headers: { 'X-CSRFToken': csrftoken }
    });
        // Get the prompt
        var prompt = $('#prompt').val();
        var dateTime = new Date();
        var time = dateTime.toLocaleTimeString();
        // Add the prompt to the response div
        $('#response').append('<p>('+ time + ') <i class="bi bi-person"></i>: ' + prompt + '</p>');
        // Clear the prompt
        $('#prompt').val('');
        $.ajax({
            url: 'https://76cf-140-112-41-151.ngrok-free.app/petlover/callback',
            type: 'POST',
            data: {prompt: prompt},
            dataType: 'json',
            success: function(data) {
                $('#response').append('<p>('+ time + ') <i class="bi bi-robot"></i>: ' + data.response + '</p>');
            }
        });
    });
});
