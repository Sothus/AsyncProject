from channels import Group
from .models import Product
import decimal

def ws_connect(message):
	print("Someone connected")
	path = message['path']
	print(path)
	if path == '/dummy_auction/':
		print("Adding new user to auction group")
		Group("auction").add(message.reply_channel)
		message.reply_channel.send({
			"text": "You're connected to group",
		})
	else:
		print("stranger!")



def ws_message(message):
	print("Received!" + message['text'])
	command = message['text']
	if command == "bid_auction":
		product = Product.objects.first()
		product.price += decimal.Decimal(0.01)
		product.save()
		Group("auction").send({"text": "[VALUE_UP]" + str(product.price),})

def ws_disconnect(message):
	print("Someone left us")
	Group('auction').discard(message.reply_channel)
