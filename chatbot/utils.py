import frappe
import os
import pdfkit
import json
from datetime import datetime
from frappe.www.printview import get_html_and_style
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
def send_document(base_html=None,name=None,options = {'orientation':'Portrait'},type = "pdf"):
    if type == "Report":
        path = os.getcwd()+frappe.utils.get_site_base_path()[1:]+"/public/files/General Ledger.pdf"
    else:
        path = os.getcwd()+frappe.utils.get_site_base_path()[1:]+"/public/files/SAL-ORD-2024-00006.pdf"
    if type == "pdf_value":
        now = datetime.now()
        now = now.strftime("%d-%m-%Y")
        statement_id =str(name)+"_"+str(now)
        path = os.getcwd()+frappe.utils.get_site_base_path()[1:]+"/public/files/"+statement_id+".pdf"
        pdfkit.from_string(base_html, path,options={'orientation':'Portrait'})
    return path
def send_file_contet(path):
    with open(path, 'rb') as file:
        return file
def get_prinformat_html(doctype,name):
    base_html=get_html_and_style(doc=doctype,name=name)
    base_html="""<html lang="en" dir="ltr"> """+base_html.get("style")+base_html.get("html")+" </html>"
    return base_html
def get_report_html(report,filters=None):
    base_html=""
    if not filters:
       filters= '{"company":"A (Demo)","from_date":"2024-08-27","to_date":"2024-09-27","group_by":"Group by Voucher (Consolidated)","include_dimensions":1,"show_opening_entries":0,"include_default_book_entries":1,"show_cancelled_entries":0,"show_net_values_in_party_account":0,"add_values_in_transaction_currency":0,"show_remarks":0,"ignore_err":0,"ignore_cr_dr_notes":0}'
    if report == "General Ledger":
        report_get_htm_doc=frappe.new_doc("Auto Email Report")
        report_get_htm_doc.report=report
        report_get_htm_doc.filters =filters
        report_get_htm_doc.report_type="Script Report"
        report_get_htm_doc.user="Administrator"
        report_get_htm_doc.name="General Ledger"
        report_get_htm_doc.description="General Ledger"
        report_get_htm_doc.format = "HTML"
        base_html=report_get_htm_doc.get_report_content()
    return base_html
