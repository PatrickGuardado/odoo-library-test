import json
from odoo import http
from odoo.http import request, Response

class LibraryPortal(http.Controller):
    
    @http.route(['/my/loans'], type='http', auth="user", website=True)
    def portal_my_loans(self, **kw):
        # Buscamos los préstamos del usuario que ha iniciado sesión
        loans = request.env['library.loan'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        return request.render("library_management.portal_my_loans", {
            'loans': loans,
            'page_name': 'loan',
        })

    @http.route(['/my/loans/renew/<int:loan_id>'], type='http', auth="user", website=True)
    def portal_renew_loan(self, loan_id, **kw):
        # sudo() nos permite saltar la seguridad temporalmente para modificar el préstamo desde el portal
        loan = request.env['library.loan'].sudo().browse(loan_id)
        
        # Validamos que el préstamo sea del usuario actual y esté activo
        if loan.exists() and loan.partner_id.id == request.env.user.partner_id.id:
            if loan.state == 'active':
                loan.action_renew_loan()
                
        return request.redirect('/my/loans')

class LibraryAPI(http.Controller):

    # Endpoint GET público
    @http.route('/api/library/book/<string:isbn>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_book_by_isbn(self, isbn, **kwargs):
        # Buscamos el libro saltando reglas de seguridad (sudo) ya que es un endpoint público
        book = request.env['library.book'].sudo().search([('isbn', '=', isbn)], limit=1)
        
        # Retornamos error 404 si no existe
        if not book:
            return Response(
                json.dumps({'error': 'Libro no encontrado para el ISBN proporcionado.'}), 
                status=404, 
                mimetype='application/json'
            )

        # Retornamos los datos si existe
        data = {
            'book_id': book.id,
            'title': book.name,
            'isbn': book.isbn,
            'state': book.state,
            'availability_status': 'Disponible' if book.state == 'available' else 'No Disponible / Prestado'
        }
        
        return Response(
            json.dumps(data), 
            status=200, 
            mimetype='application/json'
        )