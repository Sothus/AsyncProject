from auctionhouse.consumer import ws_message, ws_connect, ws_disconnect

channel_routing = {
	'websocket.connect': ws_connect,
	'websocket.receive': ws_message,
	'webspcket.disconnect': ws_disconnect,

}
