from odoo import http
from odoo.http import request

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