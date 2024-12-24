# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


class ChatbotPartyType(Document):
	def validate(self):
		create_customer_custom_field(self.party_name)

def create_customer_custom_field(party_name):
	enable_telegram,enable_whatsapp,enable_slack=frappe.db.get_value("Chatbot Setup","Chatbot Setup",["enable_telegram","enable_whatsapp","enable_slack"])
	custom_fields = {}
	if enable_telegram:
		custom_fields.update( {
			party_name: [
				dict(
					fieldname="chatbot_details",
					label="Chatbot Details",
					fieldtype="Tab Break",
				),
				dict(
					fieldname="telegram_username",
					label="Telegram Username",
					fieldtype="Data",
					insert_after="chatbot_details",
				),
				dict(
					fieldname="telegram_user_id",
					label="Telegram User ID",
					read_only=1,
					label="",
					fieldtype="Data",
					insert_after="telegram_username",
				),
			]
		})
	create_custom_fields(custom_fields, update=True)
