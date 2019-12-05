(function($) {
    const button = $('#form-submit');

    button.on('click', function (event) {
        event.preventDefault();
        button.addClass('btn-warning');
        button.removeClass('btn-dark');
        const form = $('#nodemcu-form')[0];
        fetch(url, {
            method: 'post',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: new FormData(form),
        }).then(response => {
            button.removeClass('btn-warning');

            if (response.status === 200) {
                button.addClass('btn-success');
            } else {
                button.addClass('btn-danger');
            }

            setTimeout(function() {
                button.addClass('btn-dark');
                button.removeClass('btn-success');
                button.removeClass('btn-danger');
            }, 2000);
        });
    });
})(jQuery);
