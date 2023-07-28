
$(document).ready(function() {
    // Send the form on enter keypress and avoid if shift is pressed
    $('#storename').keypress(function(event) {
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
        // Get store information, curretly only find the most matched name among  the list
        var settings4js = {{ settings4js|safe }};
	var store_name = $('#storename').val();
        var mode_hint = "%petfriendly%";
	var txt = mode_hint+store_name;
	var dateTime = new Date();
        var time = dateTime.toLocaleTimeString();
        // Add theinput msg to the response div
        $('#response').append('<p>('+ time + ') <i class="bi bi-person"></i>: ' + store_name + '</p>');
        // Clear the store name input box
        $('#storename').val('');
        $.ajax({
            url: settings4js.url_pet_friendly,
            type: 'POST',
            data: {txt: txt},
            dataType: 'json',
            success: function(data) {
                $('#response').append('<p>('+ time + ') <i class="bi bi-robot"></i>: ' + data.response + '</p>');
            }
        });
    });
});
