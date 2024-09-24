import frappe
import json
from chatbot.api.telegram_api import TelegramAPI
from chatbot.chatbot.doctype.chatbot_log.chatbot_log import log_chatbot

@frappe.whitelist(allow_guest=True)
def telegram_webhook():
    """Webhook endpoint for Telegram."""
    try:
        update = frappe.request.get_json()
        api = TelegramAPI(update)

        try:
            api.process_update()
        except Exception as e:
            frappe.log_error(f"Error processing update: {str(e)}", "Telegram API Error")
            api.send_message(text="Something went wrong, Kindly contact your admin")

        return {"status": "success"}, 200

    except Exception as e:
        # Log the error and return an error response
        frappe.log_error(f"Error processing webhook: {str(e)}", "Telegram Webhook Error")

        return {"status": "error", "message": "Failed to process update"}, 500