# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.safe_exec import run_script


class ChatbotMessageTemplate(Document):
	def get_rendered_template(self, **kwargs):
		if self.enable_dynamic_response and self.template:
			if not self.is_custom_function:
				template_data = self.execute_server_script(**kwargs)

				return self.template.format(**template_data).strip()

	def execute_server_script(self, **kwargs):
		api_method = frappe.db.get_value('Server Script',
						{'name':self.server_script, 'script_type':'API'},
						'api_method')

		if api_method:
			response = run_script(self.server_script, **kwargs).get('response')

			return response