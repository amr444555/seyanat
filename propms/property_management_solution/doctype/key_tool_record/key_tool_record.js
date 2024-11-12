frappe.ui.form.on('Key Tool Record', {
    refresh: function(frm) {
        frm.trigger('set_queries');
    },

    set_queries: function(frm) {
        frm.set_query('key', function() {
            return {
                filters: {
                    'docstatus': 0
                }
            };
        });

        frm.set_query('tool', function() {
            return {
                filters: {
                    'docstatus': 0
                }
            };
        });
    },

    key: function(frm) {
        if (frm.doc.key) {
            frm.set_value('tool', '');
            frm.set_value('item', '');
            frappe.db.get_value('Key', frm.doc.key, 'property', function(r) {
                if (r && r.property) {
                    frm.set_value('property', r.property);
                }
            });
        }
    },

    tool: function(frm) {
        if (frm.doc.tool) {
            frm.set_value('key', '');
            frappe.db.get_value('Tool', frm.doc.tool, ['item', 'property'], function(r) {
                if (r) {
                    frm.set_value('item', r.item);
                    frm.set_value('property', r.property);
                }
            });
        }
    }
});
frappe.ui.form.on('Key Tool Record', {
    refresh: function(frm) {
        frm.trigger('update_status_fields');
    },

    validate: function(frm) {
        if (!frm.doc.key && !frm.doc.tool) {
            frappe.throw(__('Either Key or Tool must be selected'));
        }
        if (frm.doc.key && frm.doc.tool) {
            frappe.throw(__('Cannot select both Key and Tool'));
        }
    },

    update_status_fields: function(frm) {
        let show_holder = ['Out', 'In Use'].includes(frm.doc.status);
        frm.toggle_display(['current_holder', 'holder_type'], show_holder);
        
        if (!show_holder) {
            frm.set_value('current_holder', '');
            frm.set_value('holder_type', '');
            frm.set_value('holder_contact', '');
        }
    },

    status: function(frm) {
        frm.trigger('update_status_fields');
    }
});