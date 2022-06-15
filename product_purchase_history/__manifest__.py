{
    "name": "Purchase History",
    "version": "14.0.1.0.0",
    "category": "purchase",
    "author": "Juan David Pelaez",
    "depends": ["account", "purchase", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/purchase_order_view.xml",
        "views/purchase_history_wizard.xml",
    ],
    "application": True,
    "auto_install": False,
    "active": True,
}
