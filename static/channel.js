//Script file to connect to websocket and setup different event handlers.

document.addEventListener('DOMContentLoaded', () => {
    // Create variables to pass with every message
    var message_count = parseInt(document.querySelector('#message_count').value)
    const username = document.querySelector('#username').value;
    const channel_type = document.querySelector('#channel_type').value;
    const channel_name = document.querySelector('#channel_name').value;
    const channel_id = document.querySelector('#channel_id').value;
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        socket.emit('join', {
            'channel_name': channel_name,
            'channel_type': channel_type,
            'username': username,
            'channel_id': channel_id
        });
        // There is only 1 button with id comment, when user clicks on it. Send the comment to the group.
        document.querySelectorAll('#comment').forEach(button => {
            button.onclick = () => {

                const message = document.querySelector('#message').value;
                socket.emit('send message', {
                    'message': message,
                    'channel_name': channel_name,
                    'channel_type': channel_type,
                    'username': username,
                    'channel_id': channel_id
                });
                // Clear the message in the display
                document.querySelector('#message').value = '';
            };
        });
    });

    // Handler to refresh number of users connected to a particular channel. It just does all count.
    socket.on('user count updated', data => {
        document.querySelector('#total_user_count').innerHTML = data.total_user_count;
    });

    // Handler when a new message is sent from the server side.
    socket.on('new message', data => {

        var error_element = document.getElementById('error_message');
        if (typeof(error_element) != 'undefined' && error_element != null) {
            document.querySelector('#error_message').innerHTML = '';
        }

        message_count = message_count + 1;
        const new_div = document.createElement("div");
        // Only for color coding for rows alternatively
        if (message_count % 2 == 0) {
            new_div.setAttribute("class", "container darker");
        } else {
            new_div.setAttribute("class", "container");
        }

        //Prepare a new diff that will be appended at the bottom of the page just on top of the comment section
        const new_b = document.createElement("b");
        const new_em = document.createElement("em");
        const author_span = document.createElement("span");
        author_span.setAttribute("class", "author-left");
        var str = '@';
        new_b.textContent = str.concat(data.sender_name);
        var str2 = '&nbsp;&nbsp; : &nbsp;&nbsp;';

        new_em.innerHTML = str2.concat(data.message_content);
        author_span.appendChild(new_b);
        author_span.appendChild(new_em);

        const date_span = document.createElement("span");
        date_span.setAttribute("class", "time-right");
        date_span.textContent = data.message_time;

        new_div.appendChild(author_span);
        new_div.appendChild(date_span);

        var parent_container = document.getElementById("parent-container");
        parent_container.appendChild(new_div)

    });
});
