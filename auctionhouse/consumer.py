from channels import Group

def ws_connect(message):
	print("Someone connected")
	path = message['path']

	if path == b'/auction/':
		print("Adding new user to auction group")
		Group("auction").add(message.reply_channel)
		message.reply_channel.send({
			"text": "You're connected to group",
		)}
	else:
		print("stranger!")



def ws_message(message):
	print("Received!" + message['text'])


def ws_disconnect(message):
	print("Someone left us")
	Group('auction').discard(message.reply_channel)
