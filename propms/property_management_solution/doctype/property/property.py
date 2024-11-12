import frappe
from frappe.model.document import Document

class Property(Document):
    def validate(self):
        self.calculate_total_units()
        self.generate_property_name()

    def calculate_total_units(self):
        if self.is_property:
            self.total_units = self.total_floors * self.units_per_floor
        else:
            self.total_units = 1

    def generate_property_name(self):
        if self.property_type and self.property_number:
            property_type_doc = frappe.get_doc("Property Type", self.property_type)
            self.property_name = f"{property_type_doc.abbreviation}-{self.property_number}"

@frappe.whitelist()
def get_units_status_chart_data(property):
    units = frappe.get_all('Property Unit', 
                           filters={'property': property}, 
                           fields=['status'])
    
    status_count = {}
    for unit in units:
        status_count[unit.status] = status_count.get(unit.status, 0) + 1
    
    labels = list(status_count.keys())
    datasets = [{'values': list(status_count.values())}]
    
    return {'labels': labels, 'datasets': datasets}

@frappe.whitelist()
def change_property_owner(property, new_owner):
    prop = frappe.get_doc("Property", property)
    old_owner = prop.owner
    
    prop.owner = new_owner
    prop.append("ownership_history", {
        "from_date": frappe.utils.now(),
        "owner": new_owner,
        "previous_owner": old_owner
    })
    prop.save()
    
    return True

@frappe.whitelist()
def change_property_tenant(property, new_tenant):
    prop = frappe.get_doc("Property", property)
    old_tenant = prop.tenant
    
    prop.tenant = new_tenant
    prop.append("rent_history", {
        "from_date": frappe.utils.now(),
        "tenant": new_tenant,
        "previous_tenant": old_tenant
    })
    prop.save()
    
    return True

@frappe.whitelist()
def create_floors_and_units(property):
    prop = frappe.get_doc("Property", property)
    
    for floor in range(1, prop.total_floors + 1):
        floor_doc = frappe.get_doc({
            "doctype": "Property Floor",
            "property": prop.name,
            "floor_number": floor,
            "max_units": prop.units_per_floor
        }).insert()
        
        for unit in range(1, prop.units_per_floor + 1):
            unit_name = f"{prop.property_name}-{floor}-{unit}"
            frappe.get_doc({
                "doctype": "Property Unit",
                "property": prop.name,
                "floor": floor_doc.name,
                "unit_number": unit,
                "unit_name": unit_name,
                "status": "Available"
            }).insert()
    
    return True

@frappe.whitelist()
def generate_property_name(property_type, property_number):
    property_type_doc = frappe.get_doc("Property Type", property_type)
    return f"{property_type_doc.abbreviation}-{property_number}"