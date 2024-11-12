import frappe
from frappe.model.document import Document

class Meter(Document):
    def validate(self):
        self.validate_meter_number()

    def validate_meter_number(self):
        existing_meter = frappe.db.get_value("Meter", {"meter_number": self.meter_number, "name": ("!=", self.name)})
        if existing_meter:
            frappe.throw(f"Meter number {self.meter_number} already exists for meter {existing_meter}")

    def on_update(self):
        self.update_property_meter()

    def update_property_meter(self):
        property_doc = frappe.get_doc("Property", self.property)
        existing_meter = next((m for m in property_doc.meters if m.meter == self.name), None)
        
        if existing_meter:
            existing_meter.meter_number = self.meter_number
            existing_meter.meter_phase = self.meter_phase
            existing_meter.meter_model = self.meter_model
            existing_meter.bill_system = self.bill_system
            existing_meter.meter_purpose = self.meter_purpose
        else:
            property_doc.append("meters", {
                "meter": self.name,
                "meter_number": self.meter_number,
                "meter_phase": self.meter_phase,
                "meter_model": self.meter_model,
                "bill_system": self.bill_system,
                "meter_purpose": self.meter_purpose
            })
        
        property_doc.save()