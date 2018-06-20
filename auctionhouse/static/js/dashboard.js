$(function() {

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    chatsock.onopen = function() {

    };

    chatsock.onmessage = function(message) {
        console.log("Received Sock message!");
        console.log(message);
        console.log(jQuery.type(message));
        console.log(message.data);
        var message = jQuery.parseJSON(message.data);


    };

});
