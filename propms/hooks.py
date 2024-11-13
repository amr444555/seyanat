from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "propms"
app_title = "Property Management Solution"
app_publisher = "seyanat"
app_description = "Property Management Solution"
app_icon = "octicon octicon-home"
app_color = "grey"
app_email = "amr444555@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/propms/css/propms.css"
# app_include_js = "/assets/propms/js/propms.js"

# include js, css files in header of web template
# web_include_css = "/assets/propms/css/propms.css"
# web_include_js = "/assets/propms/js/propms.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}
page_js = {
    "pos": "property_management_solution/point_of_sale.js",
    "point-of-sale": "property_management_solution/point_of_sale.js",
}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
    "Security Access Log": "public/js/security_access_log.js",
    "Sales Invoice": "property_management_solution/sales_invoice.js",
    "Journal Entry Account": "property_management_solution/journal_entry_account.js",
    "Issue": "property_management_solution/issue.js",
    "Company": "property_management_solution/company.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "propms.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "propms.install.before_install"
# after_install = "propms.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "propms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Company-default_maintenance_tax_template",
                    "Company-default_tax_account_head",
                    "Company-default_tax_template",
                    "Company-property_management_settings",
                    "Company-security_account_code",
                    "Issue Materials Detail-mateiral_request",
                    "Issue-col_brk_001",
                    "Issue-column_break_14",
                    "Issue-column_break_4",
                    "Issue-customer_feedback",
                    "Issue-defect_found",
                    "Issue-material_request",
                    "Issue-materials_billed",
                    "Issue-materials_required",
                    "Issue-person_in_charge_name",
                    "Issue-person_in_charge",
                    "Issue-property_name",
                    "Issue-section_break_15",
                    "Issue-sub_contractor_contact",
                    "Issue-sub_contractor_name",
                    "Item-reading_required",
                    "Material Request Item-material_request",
                    "Material Request-sales_invoice",
                    "Quotation-cost_center",
                    "Sales Invoice-job_card",
                    "Sales Invoice-lease_information",
                    "Sales Invoice-lease_item",
                    "Sales Invoice-lease",
                    "Sales Invoice-property",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                (
                    "Contact-department-fieldtype",
                    "Contact-department-options",
                    "Daily Checklist-default_print_format",
                    "Issue-company-fetch_from",
                    "Issue-email_account-report_hide",
                    "Issue-issue_type-in_standard_filter",
                    "Issue-issue_type-reqd",
                    "Issue-opening_date-in_list_view",
                    "Issue-priority-in_standard_filter",
                    "Issue-quick_entry",
                    "Issue-raised_by-in_list_view",
                    "Issue-raised_by-report_hide",
                    "Issue-section_break_19-collapsible",
                    "Issue-section_break_7-collapsible",
                    "Issue-status-options",
                    "Journal Entry Account-account-columns",
                    "Journal Entry Account-cost_center-columns",
                    "Key Set Detail-key_set-in_standard_filter",
                    "Key Set Detail-returned-in_standard_filter",
                    "Key Set Detail-taken_by-in_standard_filter",
                    "Lease-customer-in_list_view",
                    "Lease-customer-in_standard_filter",
                    "Lease-end_date-in_list_view",
                    "Lease-lease_customer-in_standard_filter",
                    "Lease-property_owner-in_list_view",
                    "Lease-property_owner-in_standard_filter",
                    "Lease-property_user-in_standard_filter",
                    "Lease-property-in_standard_filter",
                    "Lease-security_status-in_standard_filter",
                    "Lease-security_status-options",
                    "Lease-start_date-in_list_view",
                    "Lease-wtax_paid_by-in_standard_filter",
                    "Material Request-material_request_type-options",
                    "Property-identification_section-bold",
                    "Property-section_break_13-bold",
                    "Property-section_break_22-bold",
                    "Property-section_break_4-bold",
                    "Property-status-options",
                    "Unit Type-search_fields",
                    "Sales Invoice-property",
                ),
            ]
        ],
    },
]


doc_events = {
    "Issue": {
        "validate": [
            "propms.issue_hook.validate",
        ],
    },
    "Material Request": {
        "validate": "propms.auto_custom.makeSalesInvoice",
        "on_update": "propms.auto_custom.makeSalesInvoice",
        "on_change": "propms.auto_custom.makeSalesInvoice",
    },
    "Meter Reading": {
        "validate": "propms.property_management_solution.my_method"
    },
    "Sales Order": {
        "validate": "propms.auto_custom.validateSalesInvoiceItemDuplication"
    },
    "Key Set Detail": {"on_change": "propms.auto_custom.changeStatusKeyset"},
    "Meter Reading": {"on_submit": "propms.auto_custom.make_invoice_meter_reading"},
}

scheduler_events = {
    "daily": [
        "propms.auto_custom.statusChangeBeforeLeaseExpire",
        "propms.auto_custom.statusChangeAfterLeaseExpire",
    ],
    "cron": {"00 12 * * *": ["propms.lease_invoice.leaseInvoiceAutoCreate"]},
}


# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"propms.tasks.all"
# 	],
# 	"daily": [
# 		"propms.tasks.daily"
# 	],
# 	"hourly": [
# 		"propms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"propms.tasks.weekly"
# 	]
# 	"monthly": [
# 		"propms.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "propms.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
#override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "propms.event.get_events"
#}
# Add this line to your hooks.py to register your API

# Overriding Whitelisted Methods
# ------------------------------
# override_whitelisted_methods = {
#   "property_management_solution.property_management_solution.doctype.security_access.security_access.generate_qr_code": "propms.property_management_solution.doctype.security_access.security_access.generate_qr_code"
# }
after_install = "propms.auto_custom.after_install"

# Define the workspace for the app
workspaces = [
    {
        "label": "Property Management",
        "icon": "fa fa-cog",
        "items": [
            {
                "type": "doctype",
                "name": "Property",
                "description": _("Property database."),
            },
            {
                "type": "doctype",
                "name": "Key Tool Record",
                "description": _("Key Tool Record."),
            },
            {
                "type": "doctype",
                "name": "Key",
                "description": _("Key sets in custody."),
            },
            {
                "type": "doctype",
                "name": "Key Details",
                "description": _("Key Details."),
            },
            {
                "type": "doctype",
                "name": "Meter",
                "description": _("Meter."),
            },
            {
                "type": "doctype",
                "name": "Meter Model",
                "description": _("Meter Model."),
            },
            {
                "type": "doctype",
                "name": "Meter Purpose",
                "description": _("Meter Purpose."),
            },
            {
                "type": "doctype",
                "name": "Meter Reading",
                "description": _("Meter Reading."),
            },
            {
                "type": "doctype",
                "name": "Meter Reading Detail",
                "description": _("Meter Reading Detail."),
            },
            {
                "type": "doctype",
                "name": "Property",
                "description": _("Property."),
            },
            {
                "type": "doctype",
                "name": "Property Amenity",
                "description": _("Property Amenity."),
            },
            {
                "type": "doctype",
                "name": "Property Floor",
                "description": _("Property Floor."),
            },
            {
                "type": "doctype",
                "name": "Property Ownership History",
                "description": _("Property Ownership History."),
            },
            {
                "type": "doctype",
                "name": "Property Rent History",
                "description": _("Property Rent History."),
            },
            {
                "type": "doctype",
                "name": "Property Type",
                "description": _("Property Type."),
            },
            {
                "type": "doctype",
                "name": "Property Unit",
                "description": _("Property Unit."),
            },
            {
                "type": "doctype",
                "name": "Security Access",
                "description": _("Security Access."),
            },
            {
                "type": "doctype",
                "name": "Security Access Log",
                "description": _("Security Access Log."),
            },
            {
                "type": "doctype",
                "name": "Tool",
                "description": _("Tool."),
            },
            {
                "type": "doctype",
                "name": "Tool Detail",
                "description": _("Tool Detail."),
            },
        ]
    }
]
