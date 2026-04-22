from odoo import models, fields, api
from datetime import date

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Catálogo de Libros'

    name = fields.Char(string="Título", required=True)
    author = fields.Char(string="Autor", required=True)
    isbn = fields.Char(string="ISBN")
    publish_date = fields.Date(string="Fecha de Publicación")
    state = fields.Selection([
        ('available', 'Disponible'),
        ('borrowed', 'Prestado')
    ], default='available', string="Estado")
    
    # Campo calculado
    years_since_publish = fields.Integer(compute='_compute_years', string="Años desde publicación")

    @api.depends('publish_date')
    def _compute_years(self):
        for record in self:
            if record.publish_date:
                record.years_since_publish = date.today().year - record.publish_date.year
            else:
                record.years_since_publish = 0

    def action_create_loan(self):
        self.ensure_one() # Asegura que solo estamos operando sobre un libro
        return {
            'name': 'Registrar Préstamo',
            'type': 'ir.actions.act_window',
            'res_model': 'library.loan',
            'view_mode': 'form',
            'context': {'default_book_id': self.id}, # Pre-llena el libro automáticamente
            'target': 'new', # Abre una ventana emergente
        }