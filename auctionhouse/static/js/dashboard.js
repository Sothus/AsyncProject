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
        var i;
        var list_of_auctions = '<table class="table">';
        list_of_auctions += '<tr><th>Produkt</th><th>URL</th></tr>'
        for(i = 0; i < message.auctions.length; i++){
          console.log(message.auctions[i]);
          list_of_auctions += '<tr><td>'+ message.auctions[i].name + '</td><td>' + message.auctions[i].url + '</td></tr>'
        }
        list_of_auctions += "</table>";

        $("#auctions").html(list_of_auctions);


    };




});
