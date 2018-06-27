$(function() {

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    chatsock.onopen = function() {
           console.log("Connected!");
           $('#auction').text("Connected!");
           chatsock.send("Connected!");
           console.log(document.URL);
    };

    chatsock.onmessage = function(message) {
        console.log("Received Sock message!");
        console.log(message);
        console.log(jQuery.type(message));
        console.log(message.data);
        var message = jQuery.parseJSON(message.data);
        console.log(message.action);
        if(message.action == 'VALUE_UP')
        {
          console.log("trolololo");
    			$('.price').text(message.user + " bids: " + parseFloat(message.value).toFixed(2) + "$");
    		}
    };

    $(document).on("mousedown", ".bid_auction", function(){
      console.log("mousedown");
      chatsock.send("bid_auction");
    });
});
