import frappe
from frappe import _
from frappe.model.document import Document

class SecurityAccess(Document):
    def validate(self):
        self.validate_property()
        self.validate_duplicate_access()
    
    def validate_property(self):
        if self.property:
            property_status = frappe.db.get_value('Property', self.property, 'status')
            if property_status != 'Active':
                frappe.throw(_('Selected property must be active'))
    
    def validate_duplicate_access(self):
        filters = {
            'property': self.property,
            'access_type': self.access_type,
            'name': ['!=', self.name]
        }
        if frappe.db.exists('Security Access', filters):
            frappe.throw(_('Similar access already exists for this property'))