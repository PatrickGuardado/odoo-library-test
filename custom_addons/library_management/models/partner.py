from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    library_code = fields.Char(string="Código de Socio", readonly=True, copy=False, default="Nuevo")
    join_date = fields.Date(string="Fecha de Alta", default=fields.Date.today)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('library_code', 'Nuevo') == 'Nuevo':
                vals['library_code'] = self.env['ir.sequence'].next_by_code('res.partner.library.code') or 'Nuevo'
        return super(ResPartner, self).create(vals_list)