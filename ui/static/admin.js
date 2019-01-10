// Create alert, show it and handle close
function makeAlert(message, category) {
    var alert = $('<li class="alert alert-' + category + ' alert-dismissible fade show" role="alert">' + message +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span></button></li>');
    $(".alert-list").append(alert);

    // Close alert after 4s
    window.setTimeout(function () {
        alert.alert('close');
    }, 4000);
    return alert;
}

// Handle AJAX form responses
function formHandler(resp, status, on_success, on_failed, on_error) {
    console.log(resp); //TODO remove me
    if (status === 'success') {
        if (resp.status === 'success') {
            on_success(resp, status);
        } else if (resp.status === 'failed') {
            on_failed(resp.reason)
        } else if (resp.status === 'errors') {
            on_error(resp, status);
        }
    } else {
        console.log('Failed to POST form, status: ' + status);
    }
}
