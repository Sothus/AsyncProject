from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import Product
from django.contrib.auth.models import User
import json
import decimal

@channel_session_user_from_http
def ws_connect(message):
	print("User: ", message.user)
	print("Someone connected")
	product_id, product_name = get_group(message)
	auction = Product.objects.get(pk=product_id)
	if auction:
		print("Adding new user to auction id -> " + str(product_id) + "; name -> " + product_name)
		json_response = json.dumps({"action": "INFO", "user": message.user.username, "value": message.user.username + "connected to " + product_name + " auction group"})

		Group(str(product_id)).add(message.reply_channel)
		message.reply_channel.send({
			"text": json_response,
		})
	else:
		print("stranger!")

@channel_session_user
def ws_message(message):
	print("User: ", message.user)
	print("Received!" + message['text'])
	product_id, product_name = get_group(message)
	command = message['text']
	if command == "bid_auction":
		product = Product.objects.get(pk=product_id)
		bidder = User.objects.get(username=message.user)
		product.price += decimal.Decimal(0.01)
		product.current_bidder = bidder
		product.save()
		json_response = json.dumps({"action": "VALUE_UP", "user": message.user.username, "value": str(product.price),})
		Group(str(product_id)).send({"text": json_response,})

@channel_session_user
def ws_disconnect(message):
	print("User: ", message.user)
	print("Someone left us")
	Group('auction').discard(message.reply_channel)


def get_group(message):
	'''Function gets auction id and name from the WebSocket message

	Keywords arguments:
		message -- Channels.Message object

	Returns:
		auction_id, auction_name
	'''
	message_path = message['path']
	splitted_path = message_path.split('/')
	auction_id = splitted_path[1]
	auction_name = splitted_path[2]

	return auction_id, auction_name
