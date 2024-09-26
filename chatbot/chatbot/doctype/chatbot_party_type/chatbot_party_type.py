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
	insert_afrter_fieldname= frappe.get_meta(party_name)
	insert_afrter_fieldname=insert_afrter_fieldname.fields[-1].get("fieldname")
	print(insert_afrter_fieldname)
	custom_fields = {}
	if enable_telegram:
		custom_fields = {
			party_name: [
				dict(
					fieldname="chatbot_details",
					label="Chatbot Details",
					fieldtype="Tab Break",
					insert_afrter=insert_afrter_fieldname,
				),
				dict(
					fieldname="sb_chb",
					label="",
					fieldtype="Section Break",
					insert_afrter="chatbot_details"
				),
				dict(
					fieldname="telegram_username",
					label="Telegram Username",
					fieldtype="Data",
					insert_after="sb_chb",
				),
				dict(
					fieldname="telegram_user_id",
					read_only=1,
					label="",
					fieldtype="Data",
					insert_after="telegram_username",
				),
			]
		}
		print(custom_fields)
	create_custom_fields(custom_fields, update=True)