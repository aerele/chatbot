from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def customer_field_customization():
	create_customer_custom_field()

def create_customer_custom_field():
	custom_fields = {
		"Customer": [
			dict(
				fieldname="custom_telegram_username",
				label="Telegram Username",
				fieldtype="Data",
				insert_after="customer_group",
			),
			dict(
				fieldname="telegram_user_id",
				read_only=1,
				label="",
				fieldtype="Data",
				insert_after="custom_telegram_username",
			),
		]
	}
	create_custom_fields(custom_fields, update=True)