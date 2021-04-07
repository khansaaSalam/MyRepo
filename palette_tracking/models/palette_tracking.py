import logging
from odoo import _, api, fields, models, modules, tools
from odoo.exceptions import AccessError, UserError

_logger = logging.getLogger(__name__)


class PaletteTracking(models.Model):
    _name = 'palette.tracking'
    _rec_name ='icense_plate'

    picking_id = fields.Many2one('stock.picking', required=True)
    partner_id = fields.Many2one('res.partner', "Partner", default=lambda self: self.env.user.partner_id)
    icense_plate = fields.Char("Icense Plate")
    picking_partner_id = fields.Many2one('res.partner', "Picking Partner")
    picking_date_done = fields.Datetime("Picking Date Done")
    palette_count_plus = fields.Integer("Palette Count Plus")
    palette_count_minus = fields.Integer("Palette Count Minus")
    balance = fields.Integer("Balance", compute="compute_balance")

    @api.depends('palette_count_plus', 'palette_count_minus')
    def compute_balance(self):
        for rec in self:
            rec.balance = rec.palette_count_plus - rec.palette_count_minus

    @api.onchange('picking_id')
    def picking(self):
        for rec in self:
            rec.picking_date_done = rec.picking_id.date_done
            rec.picking_partner_id = rec.picking_id.partner_id


