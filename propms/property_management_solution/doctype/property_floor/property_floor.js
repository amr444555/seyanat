frappe.ui.form.on('Property Floor', {
    setup: function(frm) {
        frm.set_query("property", function() {
            return {
                filters: {
                    "is_property": 1
                }
            };
        });
    }
});