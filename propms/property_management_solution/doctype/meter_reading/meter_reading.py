import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import add_days
from propms.auto_custom import get_item_details, get_latest_active_lease, make_invoice, get_tax, getDueDate, get_cost_center

class MeterReading(Document):
    def validate(self):
        self.calculate_consumption()
        self.update_meter()

    def calculate_consumption(self):
        last_reading = frappe.get_all(
            "Meter Reading",
            filters={"meter": self.meter, "reading_date": ("<", self.reading_date)},
            fields=["reading_value", "reading_date"],
            order_by="reading_date desc",
            limit=1
        )

        if last_reading:
            last_reading = last_reading[0]
            self.consumption = self.reading_value - last_reading.reading_value
            days_between = (datetime.strptime(str(self.reading_date), "%Y-%m-%d") - 
                            datetime.strptime(str(last_reading.reading_date), "%Y-%m-%d")).days
            self.days_since_last_reading = days_between
            self.average_monthly_consumption = (self.consumption / days_between) * 30 if days_between > 0 else 0

            self.append("reading_details", {
                "previous_reading_date": last_reading.reading_date,
                "previous_reading_value": last_reading.reading_value,
                "consumption": self.consumption,
                "days_between_readings": days_between,
                "average_monthly_consumption": self.average_monthly_consumption
            })
        else:
            self.consumption = 0
            self.days_since_last_reading = 0
            self.average_monthly_consumption = 0

    def update_meter(self):
        frappe.db.set_value("Meter", self.meter, {
            "last_reading_date": self.reading_date,
            "last_reading_value": self.reading_value
        })

    @frappe.whitelist()
    def make_invoice_meter_reading(self):
        meter_doc = frappe.get_doc("Meter", self.meter)
        property_doc = frappe.get_doc("Property", meter_doc.property)
        
        item_detail = self.get_item_details()
        lease = frappe.get_doc("Lease", get_latest_active_lease(property_doc.name))
        customer = lease.customer

        if customer:
            invoice_number = make_invoice(
                self.reading_date,
                customer,
                property_doc.name,
                item_detail,
                meter_doc.meter_purpose,
                self.reading_details[0].previous_reading_date if self.reading_details else None,
                self.reading_date
            )
            return invoice_number
        else:
            frappe.throw("No active lease found for the property.")

    def get_item_details(self):
        return get_item_details(
            self.meter.meter_purpose,
            self.consumption,
            self.reading_details[0].previous_reading_date if self.reading_details else None,
            self.reading_date
        )