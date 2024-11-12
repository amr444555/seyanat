import frappe
from frappe.model.document import Document

class KeyToolRecord(Document):
    def validate(self):
        self.validate_key_or_tool()
        self.update_status()
        self.validate_key_tool_selection()
        self.validate_holder_details()
        self.update_parent_status()

    def validate_key_or_tool(self):
        if not self.key and not self.tool:
            frappe.throw("Either Key or Tool must be specified")
        if self.key and self.tool:
            frappe.throw("Only one of Key or Tool can be specified")

    def update_status(self):
        if self.key:
            self.update_key_status()
        elif self.tool:
            self.update_tool_status()

    def update_key_status(self):
        key_doc = frappe.get_doc("Key", self.key)
        key_detail = next((d for d in key_doc.key_details if d.key_number == self.key_number), None)
        if key_detail:
            key_detail.status = self.status
            key_detail.current_holder = self.current_holder
            key_detail.holder_type = self.holder_type
            key_detail.holder_contact = self.holder_contact
            key_detail.keeping_location = self.keeping_location
            key_doc.save()

    def validate(self):
        self.validate_key_tool_selection()
        self.validate_holder_details()
        self.update_parent_status()
    
    def validate_key_tool_selection(self):
        if not self.key and not self.tool:
            frappe.throw(_("Either Key or Tool must be selected"))
        if self.key and self.tool:
            frappe.throw(_("Cannot select both Key and Tool"))
    
    def validate_holder_details(self):
        if self.status in ['Out', 'In Use']:
            if not self.holder_type:
                frappe.throw(_("Holder Type is required when status is Out or In Use"))
            if not self.current_holder and self.holder_type != 'Other':
                frappe.throw(_("Current Holder is required"))
            if self.holder_type == 'Other' and not self.holder_contact:
                frappe.throw(_("Holder Contact is required for Other holder type"))
    
    def update_parent_status(self):
        if self.key:
            frappe.get_doc("Key", self.key).run_method("update_key_status")
        elif self.tool:
            frappe.get_doc("Tool", self.tool).run_method("update_tool_status")        

    def update_tool_status(self):
        tool_doc = frappe.get_doc("Tool", self.tool)
        tool_detail = next((d for d in tool_doc.tool_details if d.tool_number == self.tool_number), None)
        if tool_detail:
            tool_detail.status = self.status
            tool_detail.current_holder = self.current_holder
            tool_detail.holder_type = self.holder_type
            tool_detail.holder_contact = self.holder_contact
            tool_detail.keeping_location = self.keeping_location
            tool_doc.save()

@frappe.whitelist()
def get_key_tool_details(key=None, tool=None):
    if key:
        return frappe.get_doc("Key", key)
    elif tool:
        return frappe.get_doc("Tool", tool)
    else:
        return None