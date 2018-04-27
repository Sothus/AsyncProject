from channels import Group
from .models import Product
import decimal


def ws_connect(message):
	print("Someone connected")
	product_id, product_name = get_group(message)
	auction = Product.objects.get(pk=product_id)
	if auction:
		print("Adding new user to auction id -> " + str(product_id) + "; name -> " + product_name)
		Group(str(product_id)).add(message.reply_channel)
		message.reply_channel.send({
			"text": "You're connected to " + product_name + " auction group",
		})
	else:
		print("stranger!")


def ws_message(message):
	print("Received!" + message['text'])
	product_id, product_name = get_group(message)
	command = message['text']
	if command == "bid_auction":
		product = Product.objects.get(pk=product_id)
		product.price += decimal.Decimal(0.01)
		product.save()
		Group(str(product_id)).send({"text": "[VALUE_UP]" + str(product.price),})


def ws_disconnect(message):
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
