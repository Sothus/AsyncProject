$(function() {

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/dummy_auction/");

    chatsock.onopen = function() {
           console.log("Connected!");
           $('#auction').text("Connected!");
           chatsock.send("Connected!");
    };

    chatsock.onmessage = function(message) {
        console.log("Received Sock message!");
        console.log(message);
    };

    $(document).on("mousedown", ".bid_auction", function(){
      console.log("mousedown");
      chatsock.send("bid_auction");
    });
});
