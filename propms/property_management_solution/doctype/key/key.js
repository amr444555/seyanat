frappe.ui.form.on('Key', {
    refresh: function(frm) {
        frm.add_custom_button(__('Create Key Tool Record'), function() {
            frappe.new_doc('Key Tool Record', {
                key: frm.doc.name,
                property: frm.doc.property
            });
        });
        frm.trigger('update_key_status');
    },
    
    update_key_status: function(frm) {
        let available = 0;
        let out = 0;
        let lost = 0;
        
        frm.doc.key_details.forEach(function(key) {
            if (key.status === 'Available') available++;
            else if (key.status === 'Out') out++;
            else if (key.status === 'Lost') lost++;
        });
        
        frm.set_value('available_keys', available);
        frm.set_value('out_keys', out);
        frm.set_value('lost_keys', lost);
    },
    
    key_details_add: function(frm) {
        frm.trigger('update_key_status');
    },
    
    key_details_remove: function(frm) {
        frm.trigger('update_key_status');
    }
});

frappe.ui.form.on('Key Detail', {
    status: function(frm, cdt, cdn) {
        frm.trigger('update_key_status');
    }
});

frappe.ui.form.on('Key', {
    refresh: function(frm) {
        // ... existing refresh function ...

        // Refresh the form when a new Key Tool Record is added
        frm.doc.key_tool_records.forEach(function(record) {
            frappe.model.with_doc('Key Tool Record', record.name, function() {
                var key_tool_record = frappe.model.get_doc('Key Tool Record', record.name);
                frm.refresh_field('key_tool_records');
                frm.trigger('update_key_status');
            });
        });
    },
    // ... other existing functions ...
});