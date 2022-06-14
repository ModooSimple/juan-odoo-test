from odoo import api, fields, models


class PurchaseHistoryWizard(models.TransientModel):
    _name = "purchase.history.wizard"

    def _get_purchase_line(self):
        return self.env["purchase.order.line"].browse(self._context.get("active_id"))

    @api.model
    def _default_product_id(self):
        line = self._get_purchase_line()
        return line.product_id

    @api.model
    def _get_purchase_invoice_lines(self):
        purchase_line = self._get_purchase_line()
        product_id = purchase_line.product_id.id
        purchase_lines = self.env["purchase.order.line"].search(
            [("product_id", "=", product_id)]
        )
        purchase_history_lines = purchase_lines.invoice_lines.filtered(
            lambda line: line.parent_state == "posted" and line.quantity > 0
        )
        return purchase_history_lines

    @api.model
    def _default_purchase_history_lines(self):
        purchase_history_lines = self._get_purchase_invoice_lines()
        vals = []
        for line in purchase_history_lines:
            invoice_id = line.move_id
            order_line_id = line.purchase_line_id
            order_id = order_line_id.order_id

            invoice_number = line.move_name
            invoice_date = invoice_id.date
            vendor = line.partner_id.name
            order_number = order_id.name
            order_date = order_line_id.date_order
            qty_ordered = order_line_id.product_qty
            qty_received = order_line_id.qty_received
            qty_billed = line.quantity
            product_uom = line.product_uom_id
            price_unit = line.price_total / (
                round(product_uom.factor_inv) * line.quantity
            )
            subsidiary = order_id.picking_type_id.warehouse_id.name

            vals.append(
                (
                    0,
                    0,
                    {
                        "invoice_number": invoice_number,
                        "invoice_date": invoice_date,
                        "vendor": vendor,
                        "order_number": order_number,
                        "order_date": order_date,
                        "qty_ordered": qty_ordered,
                        "qty_received": qty_received,
                        "qty_billed": qty_billed,
                        "product_uom": product_uom.name,
                        "price_unit": price_unit,
                        "subsidiary": subsidiary,
                    },
                )
            )
        return vals

    product_id = fields.Many2one("product.product", string="Product")
    purchase_lines = fields.One2many(
        "purchase.history.line.wizard",
        "wiz_id",
        string="Purchase History",
        default=_default_purchase_history_lines,
    )


class PurchaseHistoryLineWizard(models.TransientModel):
    _name = "purchase.history.line.wizard"
    _order = "date desc"

    wiz_id = fields.Many2one("purchase.history.wizard")
    invoice_number = fields.Char("Invoice Number")
    invoice_date = fields.Datetime("Invoice Date")
    vendor = fields.Char("Vendor")
    order_number = fields.Char("Purchase Number")
    order_date = fields.Datetime("Purchase Date")
    qty_ordered = fields.Float("Ordered Qty")
    qty_received = fields.Float("Received Qty")
    qty_billed = fields.Float("Billed Qty", help="Quantity billed in invoice")
    product_uom = fields.Char("UoM")
    price_unit = fields.Float("Net cost")
    subsidiary = fields.Char("Subsidiary")
