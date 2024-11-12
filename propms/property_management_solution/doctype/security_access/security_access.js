frappe.ui.form.on('Security Access', {
    refresh: function(frm) {
        frm.trigger('validate_status');
    },
    
    validate_status: function(frm) {
        if (frm.doc.status === 'Inactive') {
            frappe.msgprint({
                title: __('Warning'),
                indicator: 'orange',
                message: __('This access point is currently inactive')
            });
        }
    },
    
    property: function(frm) {
        if (frm.doc.property) {
            frappe.db.get_value('Property', frm.doc.property, 'status')
                .then(r => {
                    if (r.message && r.message.status !== 'Active') {
                        frappe.throw(__('Selected property is not active'));
                    }
                })
                .catch(err => {
                    frappe.throw(__('Error validating property status'));
                });
        }
    }
});