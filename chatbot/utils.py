import frappe

def validate_user(user_name:str, service_name:str):
    party_list = frappe.db.get_all("Chatbot Party Type", pluck="name")

    if service_name == "Telegram":
        for party in party_list:
            party_name = frappe.db.get_value(party, {"telegram_username":user_name})
            if party_name:
                return party, party_name

    return None, None


def get_root_chatbot_flow(party_type):
    party_tree=frappe.db.get_all("Chatbot Associated Party Types",{"parent":["is","set"],"parenttype":"Chatbot Flow","party_name": party_type},["parent"],pluck="parent")
    root_doc = frappe.db.get_value('Chatbot Flow',
                              {'parent_chatbot_flow': ["is", "null"], 'button_text' : ["is", "null"],"name":["in",party_tree]},
                              ['template', 'name'], as_dict=1)

    if root_doc:
        return root_doc
    else:
        frappe.throw("No root document found for Chatbot Flow.", exc=frappe.DoesNotExistError)


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
