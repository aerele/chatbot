import frappe
import json
from chatbot.api.telegram_api import TelegramAPI

@frappe.whitelist(allow_guest=True)
def telegram_webhook():
    """Webhook endpoint for Telegram."""
    try:
        update = frappe.request.get_json()
        api = TelegramAPI()
        api.process_update(update)

        return {"status": "success"}, 200

    except Exception as e:
        # Log the error and return an error response
        frappe.log_error(f"Error processing webhook: {str(e)}", "Telegram Webhook Error")
        return {"status": "error", "message": "Failed to process update"}, 500