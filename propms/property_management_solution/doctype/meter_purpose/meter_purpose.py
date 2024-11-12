import frappe
from frappe import _
from frappe.model.document import Document

class MeterPurpose(Document):
    def validate(self):
        self.validate_duplicate_purpose()
    
    def validate_duplicate_purpose(self):
        if frappe.db.exists("Meter Purpose", {
            "purpose": self.purpose,
            "name": ("!=", self.name)
        }):
            frappe.throw(_("Purpose already exists"))