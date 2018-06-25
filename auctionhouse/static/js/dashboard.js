$(function() {

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    function send_request(){
      chatsock.send("get_user_bid_auctions");
    }

    chatsock.onopen = function() {
      console.log("Connected!");
      chatsock.send("Connected!");
      console.log(document.URL)
      var intervalID = setInterval(send_request, 5000);
    };

    chatsock.onmessage = function(message) {
        console.log("Received Sock message!");
        console.log(message);
        console.log(jQuery.type(message));
        console.log(message.data);
        var message = jQuery.parseJSON(message.data);


    };




});
