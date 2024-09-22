import frappe

def validate_user(user_name:str, service_name:str):
    try:
        party_list = frappe.db.get_all("Chatbot Party Type", pluck="name")

        if service_name == "Telegram":
            for party in party_list:
                party_name = frappe.db.get_value(party, {"custom_telegram_username":user_name})
                if party_name:
                    return party, party_name

        return None, None

    except Exception as e:
        frappe.throw("Validate User Error", e)


def get_root_chatbot_flow():
    root_doc = frappe.db.get_all('Chatbot Flow',
                              filters={'parent_chatbot_flow': '', 'button_text' : ''},
                              fields=['template', 'name'])

    if root_doc:
        return root_doc[0]  # Return the first root document found
    else:
        frappe.throw("No root document found for Chatbot Flow.")


def get_associated_party_types(docname:str):
    party_types = frappe.db.get_all("Chatbot Associated Party Types",
                            filters={'parent':docname},
                            pluck='party_name'
                            )

    return party_types


def fetch_all_children(docname:str):
    children = frappe.db.get_all('Chatbot Flow',
                    filters={'parent_chatbot_flow':docname},
                    fields=['name', 'button_text']
                    )

    return children
