import frappe
from frappe.model.document import Document

class Tool(Document):
    def validate(self):
        self.update_tool_status()

    def update_tool_status(self):
        available = 0
        in_use = 0
        under_maintenance = 0
        out_of_service = 0
        
        for tool in self.tool_details:
            if tool.status == 'Available':
                available += 1
            elif tool.status == 'In Use':
                in_use += 1
            elif tool.status == 'Under Maintenance':
                under_maintenance += 1
            elif tool.status == 'Out of Service':
                out_of_service += 1
        
        self.available_tools = available
        self.in_use_tools = in_use
        self.under_maintenance_tools = under_maintenance
        self.out_of_service_tools = out_of_service

@frappe.whitelist()
def create_tool_movement_record(tool):
    tool_doc = frappe.get_doc("Tool", tool)
    tool_movement_record = frappe.new_doc("Key Tool Record")
    tool_movement_record.tool = tool
    tool_movement_record.item = tool_doc.item
    return tool_movement_record