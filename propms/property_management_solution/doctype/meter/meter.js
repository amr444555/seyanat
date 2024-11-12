frappe.ui.form.on('Meter', {
    refresh: function(frm) {
        // Add custom buttons or other refresh logic here
    },
    
    property: function(frm) {
        if (frm.doc.property) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Property',
                    name: frm.doc.property
                },
                callback: function(r) {
                    if (r.message) {
                        // You can set other fields based on the property if needed
                    }
                }
            });
        }
    }
});
frappe.ui.form.on('Meter', {
    refresh: function(frm) {
        try {
            if (!frm.doc.__islocal) {
                frm.add_custom_button(__('Create Meter Reading'), function() {
                    frappe.new_doc('Meter Reading', {
                        meter: frm.doc.name,
                        property: frm.doc.property
                    });
                });
            }
        } catch (error) {
            frappe.throw(__('Error creating meter reading: ') + error);
        }
    },

    validate: function(frm) {
        if (frm.doc.installation_date && frappe.datetime.get_today() < frm.doc.installation_date) {
            frappe.throw(__('Installation Date cannot be in the future'));
        }
    },

    property: function(frm) {
        if (frm.doc.property) {
            frappe.db.get_value('Property', frm.doc.property, 'status')
                .then(r => {
                    if (r.message && r.message.status !== 'Active') {
                        frappe.throw(__('Selected property must be active'));
                    }
                })
                .catch(err => {
                    frappe.throw(__('Error validating property: ') + err);
                });
        }
    }
});