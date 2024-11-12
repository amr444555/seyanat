import frappe
from frappe.model.document import Document

class Key(Document):
    def validate(self):
        self.update_key_status()

    def update_key_status(self):
        available = 0
        out = 0
        lost = 0
        
        for key in self.key_details:
            if key.status == 'Available':
                available += 1
            elif key.status == 'Out':
                out += 1
            elif key.status == 'Lost':
                lost += 1
        
        self.available_keys = available
        self.out_keys = out
        self.lost_keys = lost

@frappe.whitelist()
def create_key_tool_record(key):
    key_doc = frappe.get_doc("Key", key)
    key_tool_record = frappe.new_doc("Key Tool Record")
    key_tool_record.key = key
    key_tool_record.property = key_doc.property
    return key_tool_record