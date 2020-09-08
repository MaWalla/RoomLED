(function($) {
    const submitButton = $('#form-submit');
    const offButton = $('#off-button');

    const sendRequest = (button, data) => {
        button.addClass('btn-warning');
        button.removeClass('btn-dark');

        fetch(url, {
            method: 'post',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: data,
        }).then(response => {
            button.removeClass('btn-warning');

            if (response.status === 200) {
                button.addClass('btn-success');
            } else {
                button.addClass('btn-danger');
            }

            setTimeout(function () {
                button.addClass('btn-dark');
                button.removeClass('btn-success');
                button.removeClass('btn-danger');
            }, 2000);
        })
    };

    submitButton.on('click', function (event) {
        event.preventDefault();
        const button = $(this);
        const form = $('#nodemcu-form')[0];
        sendRequest(button, new FormData(form));
    });

    offButton.on('click', function (event) {
        event.preventDefault();
        const button = $(this);
        const domDevices = $('.checkbox');
        const data = new FormData();
        data.append('mode', 'off')
        domDevices.map(element => (data.append(domDevices[element].id, 'on')));
        sendRequest(button, data);
    });
})(jQuery);
