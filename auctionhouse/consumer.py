from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import Product, Biders
from django.contrib.auth.models import User
import json
import decimal
from django.utils import timezone

@channel_session_user_from_http
def ws_connect(message):
	print("User: ", message.user)
	print("Someone connected")
	print(message['path'])
	if 'dashboard' in message['path']:
		print("added to dashboard user group")
		Group("dashboard-%s" % message.user.username).add(message.reply_channel)
		message.reply_channel.send({
			"text": "connected to dashboard",
		})
	else:
		product_id, product_name = get_group(message)
		try:
			auction = Product.objects.get(pk=product_id)
		except Product.DoesNotExist:
			auction = None
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
		try:
			product = Product.objects.get(pk=product_id)
			bidder = User.objects.get(username=message.user)
			is_user_bids = Biders.objects.filter(product_id=product_id,users__username=message.user).count()
			print(is_user_bids)
		except Product.DoesNotExist:
			product = None
		except User.DoesNotExist:
			bidder = None
		except Biders.DoesNotExist:
			is_user_bids = None
		#biders = Biders.objects.get(product_pk=product_id)
		#is_user_bids = Biders.objects.filter(users_username=message.user).count()
		#print(is_user_bids)
		###
		if product and bidder and is_user_bids is not None:
			if is_user_bids == 0:
				biders = Biders.objects.get(product_id=product_id)
				biders.users.add(bidder)
				biders.save()
			product.price += decimal.Decimal(0.01)
			product.current_bidder = bidder
			product.save()
			json_response = json.dumps({"action": "VALUE_UP", "user": message.user.username, "value": str(product.price),})
			Group(str(product_id)).send({"text": json_response,})
		elif bidder == None:
			print("Not authorized bid!")
	elif command == "get_user_bid_auctions":
		try:
			user = User.objects.get(username=message.user)
		except:
			user = None

		if user:
			try:
				auctions = Biders.objects.filter(users__username=message.user)
			except Biders.DoesNotExist:
				auctions = None

			if auctions:
				json_auctions = {'auctions': []}
				for auction in auctions:
					ended = False
					if (timezone.now() > auction.product.ends):
						ended = True
					json_auctions['auctions'].append({"name":auction.product.name, "url":auction.product.get_absoulte_url(), 'ended': str(ended)})
				json_auctions = json.dumps(json_auctions)
				print(auctions.count())
				Group("dashboard-%s" % message.user.username).send({'text': json_auctions})
		#is_user_bids = Biders.objects.filter(users_username=message.user).count()


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
