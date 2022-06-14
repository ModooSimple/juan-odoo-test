{
    "name": "Purchase History",
    "version": "14.0.1.0.0",
    "category": "purchase",
    "author": "Juan David Pelaez",
    "depends": ["account", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/purchase_history_wizard.xml",
        "views/purchase_order_view.xml",
    ],
    "application": True,
    "auto_install": False,
    "active": True,
}
