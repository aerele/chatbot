import frappe
import requests
import json
from chatbot.chatbot.doctype.chatbot_log.chatbot_log import log_chatbot
from chatbot.utils import validate_user, get_root_chatbot_flow, get_associated_party_types, fetch_all_children
import hashlib
from passlib.context import CryptContext
passlibctx = CryptContext(schemes=["pbkdf2_sha256","argon2",], )
class TelegramAPI:
	def __init__(self, update,headers):
		print(update)
		self.update = update
		self.headers=headers
		self.validate_token=False
		secret_token_ft=self.headers.get("X-Telegram-Bot-Api-Secret-Token")
		host=self.headers.get("X-Forwarded-Host")
		proto=self.headers.get("X-Forwarded-Proto")
		if proto !="https":
			frappe.throw("Not an https Request", frappe.PermissionError)
		if host !=frappe.db.get_value("Chatbot Setup","Chatbot Setup","telegram_webhook_url").strip()[8:]:
			frappe.throw("Not an Host", frappe.PermissionError)
		if secret_token_ft:
			secret_token = frappe.get_doc("Chatbot Setup").get_password("secret_token")
			if secret_token:
				random_value=hashlib.sha256(secret_token_ft.encode())
				random_value=random_value.hexdigest()
				if passlibctx.verify(random_value,secret_token):
					self.validate_token =True
				else:
					frappe.throw("Verify Error", frappe.PermissionError)
			else:
				frappe.throw("StFxx0n0ecre Tnmx0naoke Error", frappe.PermissionError)
		else:
			frappe.throw("StFxx0n0ecre Tnmx0naoke Error FT", frappe.PermissionError)
		self.token = frappe.get_doc("Chatbot Setup").get_password('telegram_api_token')
		self.base_url = f"https://api.telegram.org/bot{self.token}/"
		self.reply_text = str()
		self.reply_markup = {}
		self.data = str()
		self.chat_id=str()
		self.message_received=str()
		
		if "callback_query" in update:
			self.callback_query =update.get('callback_query')
			self.message = self.callback_query.get('message')
			self.data =self.callback_query.get('data')
			self.chat_id = self.message.get("chat").get("id")
			self.user_name="@"+self.message.get("chat").get("username")
		elif "message" in update:
			self.message = update.get('message')

		if self.message:
			self.chat_id = self.message.get("chat").get("id")
			self.user_name = "@"+self.message["chat"]["username"]
			self.message_received=self.message.get("text")
		else:
			frappe.throw(msg="Message object not found")


	def send_message(self, text:str =None):
		"""Send a message to a Telegram chat, with optional inline buttons."""
		url = f"{self.base_url}sendMessage"
		payload = {
			"chat_id": self.chat_id,
			"text": self.reply_text,
			"reply_markup": self.reply_markup  # Inline keyboard markup
		}
		print("payload",payload)
		response = requests.post(url, json=payload)

		log_chatbot(
			title="Telegram SendMessage API",
			method="POST",
			status="Success",
			url=url,
			request=json.dumps(response.request.body.decode('utf-8'), indent=4),
			response=json.dumps(response.json(), indent=4)
			)

		# Error handling for API response
		if response.status_code != 200:
			log_chatbot(
			title="Telegram API Error",
			method="POST",
			status="Failed",
			url=url,
			request=json.dumps(response.request.body.decode('utf-8'), indent=4),
			response=json.dumps(response.json(), indent=4)
			)

			return None

		return response.json()


	def send_photo(self, chat_id, photo_url):
		"""Send a photo to a Telegram chat."""
		url = f"{self.base_url}sendPhoto"
		payload = {
			"chat_id": chat_id,
			"photo": photo_url
		}
		response = requests.post(url, json=payload)

		if response.status_code != 200:
			frappe.log_error(f"Error sending photo: {response.text}", "Telegram API Error")
			return None

		return response.json()


	def send_document(self, chat_id, file_path):
		"""Send a document (PDF or other file types) to a Telegram chat."""
		url = f"{self.base_url}sendDocument"
		with open(file_path, 'rb') as file:
			files = {'document': file}
			payload = {
				"chat_id": chat_id
			}
			response = requests.post(url, files=files, data=payload)

		if response.status_code != 200:
			frappe.log_error(f"Error sending document: {response.text}", "Telegram API Error")
			return None

		return response.json()


	def process_update(self):
		"""Process the incoming update from the Telegram webhook."""
		if self.message:
			party_type, party_name = validate_user(self.user_name, "Telegram")

			if party_type and party_name:
				self.set_chat_id(party_type,party_name)
				self.handle_message(party_type, party_name)
			else:
				self.reply_text = "User not registered"
				self.send_message(self.reply_text)


	def handle_message(self, party_type, party_name):
		"""Handle incoming messages."""
		# Determine chatbot flow and template
		print("self.data",self.data)
		self.data=self.data if frappe.db.exists("Chatbot Flow",self.data) else None
		pre_chatbot_flow_name=frappe.cache.get_value(self.chat_id)
		pre_chatbot_flow_name=pre_chatbot_flow_name if frappe.db.exists("Chatbot Flow",pre_chatbot_flow_name) else None
		print("pre_chatbot_flow_name",pre_chatbot_flow_name)
		parent_flow=get_root_chatbot_flow(party_type)
		if self.data:
			
			chatbot_flow = frappe.get_doc('Chatbot Flow', self.data) 
		elif pre_chatbot_flow_name:
			chatbot_flow = frappe.get_doc('Chatbot Flow', pre_chatbot_flow_name)
			children = fetch_all_children(chatbot_flow.get('name'))
			if children:
				chatbot_flow = frappe.get_doc('Chatbot Flow', children[0].get("name"))
			else:
				chatbot_flow= parent_flow
			
			   
		else:
			chatbot_flow=parent_flow
		
		associated_parties = get_associated_party_types(chatbot_flow.get('name'))
		children = fetch_all_children(chatbot_flow.get('name'))
		template = chatbot_flow.get('template')

		# Build reply markup (inline keyboard)
		self.reply_markup = {"inline_keyboard": [], 'resize_keyboard': True}
		print("children",children)
		print("chatbot_flow",chatbot_flow)
		default_children=[]
		if chatbot_flow.get('name') !=parent_flow.get("name"):
			default_children=[{"name":parent_flow.get("name"),"button_text":"Main Menu"}]
			children=children+default_children
		if children:
			self.reply_markup["inline_keyboard"]= [
				[{"text": child.get('button_text'), "callback_data": child.get('name')} for child in children if child.get('button_text') ]

			]

		# Check if party_type is in associated parties
		if party_type in associated_parties:
			chatbot_template = frappe.get_doc('Chatbot Message Template', template)
			kwargs = {party_type.lower(): party_name,"data":self.message_received}
			self.reply_text = chatbot_template.get_rendered_template(**kwargs)
			print("reply_text",self.reply_text)
			self.send_message()
			frappe.cache.set_value(self.chat_id,chatbot_flow.get('name'))
	def set_chat_id(self,party_type,party_name):
		chat_id =frappe.db.get_value(party_type,party_name,"telegram_user_id")
		if not chat_id or chat_id!=self.chat_id:
			frappe.db.set_value(party_type,party_name,"telegram_user_id",self.chat_id)