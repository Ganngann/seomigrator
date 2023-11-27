var socket;

function connect() {
    socket = new WebSocket('ws://' + window.location.host + '/migrator/ws/');

    socket.onopen = function(e) {
        console.log("Connection established");
    };

    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var href = data.href;
        var old_domain_http_status = data.old_domain_http_status;
        var new_domain_http_status = data.new_domain_http_status;

        // Ajoutez les nouvelles données à votre tableau ici
        console.log("message recu");
    };

    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        setTimeout(connect, 1000);  // Try to reconnect after 1 second
    };
}

connect();  // Connect when the page loads

document.querySelector('#myform').onsubmit = function(e) {
    console.log('submit');
    e.preventDefault();
    var old_domain_input = document.querySelector('#old_domain');
    var new_domain_input = document.querySelector('#new_domain');
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            'old_domain': old_domain_input.value,
            'new_domain': new_domain_input.value,
        }));
    }
};
