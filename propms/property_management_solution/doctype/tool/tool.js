frappe.ui.form.on('Tool', {
    refresh: function(frm) {
        frm.add_custom_button(__('Create Tool Movement Record'), function() {
            frappe.new_doc('Key Tool Record', {
                tool: frm.doc.name,
                item: frm.doc.item
            });
        });
        frm.trigger('update_tool_status');
    },
    
    update_tool_status: function(frm) {
        let available = 0;
        let in_use = 0;
        let under_maintenance = 0;
        let out_of_service = 0;
        
        frm.doc.tool_details.forEach(function(tool) {
            if (tool.status === 'Available') available++;
            else if (tool.status === 'In Use') in_use++;
            else if (tool.status === 'Under Maintenance') under_maintenance++;
            else if (tool.status === 'Out of Service') out_of_service++;
        });
        
        frm.set_value('available_tools', available);
        frm.set_value('in_use_tools', in_use);
        frm.set_value('under_maintenance_tools', under_maintenance);
        frm.set_value('out_of_service_tools', out_of_service);
    },
    
    tool_details_add: function(frm) {
        frm.trigger('update_tool_status');
    },
    
    tool_details_remove: function(frm) {
        frm.trigger('update_tool_status');
    }
});

frappe.ui.form.on('Tool Detail', {
    status: function(frm, cdt, cdn) {
        frm.trigger('update_tool_status');
    }
});