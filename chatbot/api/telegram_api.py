import frappe
import requests
from chatbot.utils import validate_user, get_root_chatbot_flow, get_associated_party_types, fetch_all_children

class TelegramAPI:
    def __init__(self):
        self.token = frappe.get_doc("Chatbot Setup").get_password('telegram_api_token')
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.chat_id = str()
        self.user_name = str()
        self.reply_text = str()
        self.reply_markup = {}


    def send_message(self, chat_id:str, text:str, reply_markup:list):
        """Send a message to a Telegram chat, with optional inline buttons."""
        url = f"{self.base_url}sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": reply_markup  # Inline keyboard markup
        }
        response = requests.post(url, json=payload)
        # Error handling for API response
        if response.status_code != 200:
            frappe.log_error(f"Error sending message: {response.text}", "Telegram API Error")
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


    def process_update(self, update):
        """Process the incoming update from the Telegram webhook."""
        message = {}
        data = None

        if "callback_query" in update:
            message = update.get('callback_query').get('message')
            data = update.get('callback_query').get('data')
        elif "message" in update:
            message = update.get('message')

        if message:
            self.chat_id = message["chat"]["id"]
            self.user_name = "@"+message["chat"]["username"]
            party_type, party_name = validate_user(self.user_name, "Telegram")

            if party_type and party_name:
                self.handle_message(party_type, party_name, message, data)
            else:
                self.reply_text = "User not registered"
                self.send_message(self.chat_id, self.reply_text, self.reply_markup)


    def handle_message(self, party_type, party_name, message, data=None):
        """Handle incoming messages."""
        text = message.get("text")

        # Determine chatbot flow and template
        chatbot_flow = frappe.get_doc('Chatbot Flow', data) if data else get_root_chatbot_flow()
        associated_parties = get_associated_party_types(chatbot_flow.get('name'))
        children = fetch_all_children(chatbot_flow.get('name'))
        template = chatbot_flow.get('template')

        # Build reply markup (inline keyboard)
        self.reply_markup = {"inline_keyboard": [], 'resize_keyboard': True}

        if children:
            self.reply_markup["inline_keyboard"] = [
                [{"text": child.get('button_text'), "callback_data": child.get('name')}]
                for child in children
            ]

        # Check if party_type is in associated parties
        if party_type in associated_parties:
            chatbot_template = frappe.get_doc('Chatbot Message Template', template)
            kwargs = {party_type.lower(): party_name}
            self.reply_text = chatbot_template.get_rendered_template(**kwargs)

            self.send_message(self.chat_id, self.reply_text, self.reply_markup)

        # Fallback if there's no data and text is available
        elif text and not data:
            chatbot_template = frappe.get_doc('Chatbot Message Template', template)
            kwargs = {party_type.lower(): party_name}
            self.reply_text = chatbot_template.get_rendered_template(**kwargs)

            self.send_message(self.chat_id, self.reply_text, self.reply_markup)
