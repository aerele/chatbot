from chatbot.customization.customer.custom_field import customer_field_customization
from chatbot.customization.supplier.custom_field import supplier_field_customization
from chatbot.customization.employee.custom_field import employee_field_customization

def after_migrate():
    customer_field_customization()
    supplier_field_customization()
    employee_field_customization()