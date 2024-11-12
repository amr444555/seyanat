frappe.ui.form.on('Meter Reading', {
    refresh: function(frm) {
        frm.add_custom_button(__('Generate Invoice'), function() {
            frappe.call({
                method: 'make_invoice_meter_reading',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__('Invoice {0} has been generated', [r.message]));
                    }
                }
            });
        });
    },

    meter: function(frm) {
        if (frm.doc.meter) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Meter',
                    name: frm.doc.meter
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('property', r.message.property);
                    }
                }
            });
        }
    }
});