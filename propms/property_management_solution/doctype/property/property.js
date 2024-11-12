frappe.ui.form.on('Property', {
    refresh: function(frm) {
        frm.add_custom_button(__('View Units'), function() {
            frappe.set_route('List', 'Property Unit', {'property': frm.doc.name});
        });

        // Generate and display the units chart
        frm.trigger('generate_units_chart');

        // Set up buttons
        frm.add_custom_button(__('Change Owner'), function() {
            frm.trigger('change_owner');
        });

        frm.add_custom_button(__('Change Tenant'), function() {
            frm.trigger('change_tenant');
        });

        if (frm.doc.is_property && !frm.doc.__islocal) {
            frm.add_custom_button(__('Create Floors and Units'), function() {
                frm.trigger('create_floors_and_units');
            });
        }
    },

    generate_units_chart: function(frm) {
        frappe.call({
            method: 'propms.property_management_solution.doctype.property.property.get_units_status_chart_data',
            args: {
                property: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    let chart = new frappe.Chart("#units_chart_html", {
                        data: r.message,
                        type: 'pie',
                        height: 300,
                        colors: ['#7cd6fd', '#743ee2', '#ff5858', '#ffa00a', '#28a745', '#5e64ff', '#98d85b']
                    });
                }
            }
        });
    },

    change_owner: function(frm) {
        frappe.prompt([
            {'fieldname': 'new_owner', 'fieldtype': 'Link', 'label': 'New Owner', 'options': 'Customer', 'reqd': 1}
        ],
        function(values){
            frappe.call({
                method: 'propms.property_management_solution.doctype.property.property.change_property_owner',
                args: {
                    property: frm.doc.name,
                    new_owner: values.new_owner
                },
                callback: function(r) {
                    if (r.message) {
                        frm.reload_doc();
                        frappe.show_alert({message: __('Owner changed successfully'), indicator: 'green'});
                    }
                }
            });
        },
        'Change Property Owner',
        'Submit'
        );
    },

    change_tenant: function(frm) {
        frappe.prompt([
            {'fieldname': 'new_tenant', 'fieldtype': 'Link', 'label': 'New Tenant', 'options': 'Customer', 'reqd': 1}
        ],
        function(values){
            frappe.call({
                method: 'propms.property_management_solution.doctype.property.property.change_property_tenant',
                args: {
                    property: frm.doc.name,
                    new_tenant: values.new_tenant
                },
                callback: function(r) {
                    if (r.message) {
                        frm.reload_doc();
                        frappe.show_alert({message: __('Tenant changed successfully'), indicator: 'green'});
                    }
                }
            });
        },
        'Change Property Tenant',
        'Submit'
        );
    },

    create_floors_and_units: function(frm) {
        frappe.call({
            method: 'propms.property_management_solution.doctype.property.property.create_floors_and_units',
            args: {
                property: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    frm.reload_doc();
                    frappe.show_alert({message: __('Floors and units created successfully'), indicator: 'green'});
                }
            }
        });
    },

    property_type: function(frm) {
        frm.trigger('generate_property_name');
    },

    property_number: function(frm) {
        frm.trigger('generate_property_name');
    },

    generate_property_name: function(frm) {
        if (frm.doc.property_type && frm.doc.property_number) {
            frappe.call({
                method: 'propms.property_management_solution.doctype.property.property.generate_property_name',
                args: {
                    property_type: frm.doc.property_type,
                    property_number: frm.doc.property_number
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('property_name', r.message);
                    }
                }
            });
        }
    },

    is_property: function(frm) {
        frm.toggle_reqd('total_floors', frm.doc.is_property);
        frm.toggle_reqd('units_per_floor', frm.doc.is_property);
    },

    total_floors: function(frm) {
        frm.trigger('calculate_total_units');
    },

    units_per_floor: function(frm) {
        frm.trigger('calculate_total_units');
    },

    calculate_total_units: function(frm) {
        if (frm.doc.is_property) {
            frm.set_value('total_units', frm.doc.total_floors * frm.doc.units_per_floor);
        } else {
            frm.set_value('total_units', 1);
        }
    }
});