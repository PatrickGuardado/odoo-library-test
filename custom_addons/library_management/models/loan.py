from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Préstamo de Libro'

    partner_id = fields.Many2one('res.partner', string="Socio", required=True)
    # Solo permitimos seleccionar libros que estén disponibles
    book_id = fields.Many2one('library.book', string="Libro", required=True, domain=[('state', '=', 'available')])
    loan_date = fields.Date(string="Fecha de Préstamo", default=fields.Date.context_today, required=True)
    return_date = fields.Date(string="Fecha de Devolución")
    
    state = fields.Selection([
        ('active', 'Activo'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido')
    ], string="Estado", default='active')

    # Regla 1: Límite de 5 préstamos activos por socio
    @api.constrains('partner_id', 'state')
    def _check_loan_limit(self):
        for record in self:
            if record.state in ['active', 'overdue']:
                active_loans = self.search_count([
                    ('partner_id', '=', record.partner_id.id),
                    ('state', 'in', ['active', 'overdue'])
                ])
                if active_loans > 5:
                    raise ValidationError("El socio ya tiene 5 préstamos activos. No puede realizar más préstamos.")

    # Al crear el préstamo, cambiamos el estado del libro a prestado
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.book_id.state != 'available':
                raise ValidationError("El libro seleccionado no está disponible.")
            record.book_id.state = 'borrowed'
        return records

    # Acción para devolver el libro manualmente
    def action_return_book(self):
        for record in self:
            record.state = 'returned'
            record.return_date = fields.Date.today()
            record.book_id.state = 'available'