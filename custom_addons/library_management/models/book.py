from odoo import models, fields, api
from datetime import date

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Catálogo de Libros'

    name = fields.Char(string="Título", required=True)
    author = fields.Char(string="Autor", required=True)
    isbn = fields.Char(string="ISBN")
    publish_date = fields.Date(string="Fecha de Publicación")
    # Se relaciona con el modelo de producto para integrarse con el módulo de punto de venta
    product_id = fields.Many2one('product.product', string="Producto POS", ondelete="cascade", readonly=True)
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
        self.ensure_one() # Asegura que solo se está operando sobre un libro
        return {
            'name': 'Registrar Préstamo',
            'type': 'ir.actions.act_window',
            'res_model': 'library.loan',
            'view_mode': 'form',
            'context': {'default_book_id': self.id}, # Pre-llena el libro automáticamente
            'target': 'new', # Abre una ventana emergente
        }
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Crear un producto tipo "servicio" para que no exija inventario
            product = self.env['product.product'].create({
                'name': vals.get('name', 'Libro Sin Título'),
                'type': 'service', # 'service' no requiere stock
                'available_in_pos': True,
                'list_price': 0.0, # Se asume que el precio base cero
            })
            vals['product_id'] = product.id
            
        return super().create(vals_list)
    
