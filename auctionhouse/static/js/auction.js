$(function() {

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    chatsock.onopen = function() {
           console.log("Connected!");
           $('#auction').text("Connected!");
           chatsock.send("Connected!");
           console.log(document.URL)
    };

    chatsock.onmessage = function(message) {
        console.log("Received Sock message!");
        console.log(message);
        console.log(jQuery.type(message));
        console.log(message.data)
        if(message.data.includes("[VALUE_UP]"))
          {
            var price = message.data.split("[VALUE_UP]")[1];
            console.log(price)
            $('.price').text("$" + parseFloat(price).toFixed(2));
          }
    };

    $(document).on("mousedown", ".bid_auction", function(){
      console.log("mousedown");
      chatsock.send("bid_auction");
    });
});
