# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests

class ChatbotSetup(Document):
    def autoname(self):
        """Automatically set the name by replacing spaces with hyphens in the title."""
        self.name = self.title.replace(" ", "-")

    def validate(self):
        """Validate the Telegram API token and set the webhook if needed."""
        self.validate_api_token()
        self.set_webhook()

    def validate_api_token(self):
        """Validate the Telegram API token using Telegram's getMe API."""
        if not self.has_value_changed("telegram_api_token"):
            return  # Skip validation if token hasn't changed

        frappe.db.commit() #Commit current changes to get recent decrypted token
        api_token = self.get_password("telegram_api_token")

        url = f"https://api.telegram.org/bot{api_token}/getMe"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for 4xx/5xx status codes

            data = response.json()

            # Ensure that the API response contains valid bot information
            if data.get("result", {}).get("is_bot"):
                self.telegram_username = "@" + data["result"]["username"]
            else:
                frappe.throw("The Telegram user is not a bot.")

        except requests.exceptions.RequestException as e:
            frappe.throw(f"Failed to validate Telegram API token: {e}")

    def set_webhook(self):
        """Set the Telegram webhook URL using Telegram's setWebhook API."""
        if self.has_value_changed("telegram_webhook_url"):
            api_token = self.get_password("telegram_api_token")

            webhook_url = f"{self.telegram_webhook_url}/api/method/chatbot.webhook.telegram_webhook"
            url = f"https://api.telegram.org/bot{api_token}/setWebhook?url={webhook_url}"

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises an HTTPError for 4xx/5xx status codes

            except requests.exceptions.RequestException as e:
                frappe.throw(f"Failed to set Telegram webhook: {e}")
