# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ChatbotLog(Document):
		pass


def log_chatbot(title, method=None, url=None, voucher_type=None, voucher_name=None, status=None ,request=None, response=None):
	"""_summary_

	Args:
		title (_type_): _description_
		method (_type_, optional): _description_. Defaults to None.
		voucher_type (_type_, optional): _description_. Defaults to None.
		voucher_name (_type_, optional): _description_. Defaults to None.
		status (_type_, optional): _description_. Defaults to None.
		request (_type_, optional): _description_. Defaults to None.
		response (_type_, optional): _description_. Defaults to None.
	"""
	try:
		doc = frappe.new_doc('Chatbot Log')
		doc.update({
			"title" : title,
			"method" : method,
			"url" : url,
			"voucher_type" : voucher_type,
			"voucher_name" : voucher_name,
			"status" : status,
			"request" : request,
			"response" : response
		})
		doc.save(ignore_permissions=True)

	except:
		frappe.log_error("Chatbot Log Error")
