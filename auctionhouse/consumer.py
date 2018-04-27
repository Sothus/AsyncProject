from channels import Group
from .models import Product
import decimal

def ws_connect(message):
	print("Someone connected")
	path = message['path']
	print(path)
	product_id = path.split('/')[1]
	product_name = path.split('/')[2]
	print("product id: ", product_id, product_name)
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
	print(message.keys())
	print(message['path'])
	print(message['reply_channel'])
	command = message['text']
	if command == "bid_auction":
		product = Product.objects.first()
		product.price += decimal.Decimal(0.01)
		product.save()
		Group("auction").send({"text": "[VALUE_UP]" + str(product.price),})

def ws_disconnect(message):
	print("Someone left us")
	Group('auction').discard(message.reply_channel)
