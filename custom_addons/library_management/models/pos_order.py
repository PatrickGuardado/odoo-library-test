from odoo import models, api, _
from odoo.exceptions import UserError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    # Usamos *args y **kwargs para aceptar cualquier cantidad de parámetros que Odoo envíe
    def _process_order(self, *args, **kwargs):
        # 1. Dejamos que Odoo procese la orden normalmente pasando todos los parámetros
        res = super()._process_order(*args, **kwargs)
        pos_order = self.browse(res)

        # 2. Revisamos si en la orden hay algún libro
        for line in pos_order.lines:
            book = self.env['library.book'].search([('product_id', '=', line.product_id.id)], limit=1)
            
            if book:
                # Validamos que haya un cliente seleccionado
                if not pos_order.partner_id:
                    raise UserError(_("Debe seleccionar un cliente en el POS para prestar el libro '%s'.") % book.name)
                
                # Regla: El libro debe estar disponible
                if book.state != 'available':
                    raise UserError(_("El libro '%s' ya se encuentra prestado.") % book.name)

                # Regla: Límite de 5 préstamos
                active_loans = self.env['library.loan'].search_count([
                    ('partner_id', '=', pos_order.partner_id.id),
                    ('state', 'in', ['active', 'overdue'])
                ])
                if active_loans >= 5:
                    raise UserError(_("El socio '%s' ya alcanzó el límite de 5 préstamos.") % pos_order.partner_id.name)

                # 3. Si pasa las validaciones, creamos el préstamo
                self.env['library.loan'].create({
                    'partner_id': pos_order.partner_id.id,
                    'book_id': book.id,
                })

        return res