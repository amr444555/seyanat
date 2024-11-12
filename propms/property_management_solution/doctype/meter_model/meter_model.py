import frappe
from frappe import _
from frappe.model.document import Document

class MeterModel(Document):
    def validate(self):
        self.validate_duplicate_model()
    
    def validate_duplicate_model(self):
        if frappe.db.exists("Meter Model", {
            "model_name": self.model_name,
            "name": ("!=", self.name)
        }):
            frappe.throw(_("Model name already exists"))