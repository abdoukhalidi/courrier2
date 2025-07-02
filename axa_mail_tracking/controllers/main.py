from odoo import http
from odoo.http import request

class MailTrackingAPI(http.Controller):

    @http.route('/api/courrier/scan', type='json', auth='user', methods=['POST'])
    def scan_qr_code(self, qr_data, **kwargs):
        # Recherche du courrier par QR code
        mail = request.env['axa.mail.tracking'].sudo().search([
            ('qr_content', '=', qr_data)
        ], limit=1)

        if not mail:
            # Retourne une réponse d'erreur au format JSON
            return {
                'error': 'Courrier non trouvé',
                'status': 404
            }

        # Retourne les données du courrier
        return {
            'id': mail.id,
            'name': mail.name,
            'type': mail.mail_type,
            'sender': mail.sender,
            'status': mail.state,
            'last_update': mail.dispatch_history[0].timestamp if mail.dispatch_history else None
        }

    @http.route('/api/courrier/update', type='json', auth='user', methods=['POST'])
    def update_status(self, mail_id, action, **kwargs):
        mail = request.env['axa.mail.tracking'].sudo().browse(mail_id)
        if not mail.exists():
            return {
                'error': 'Courrier non trouvé',
                'status': 404
            }

        # Traitement des actions
        if action == 'validate':
            mail.action_validate()
        elif action == 'reject':
            mail.action_reject()
        elif action == 'dispatch':
            mail.action_dispatch()
        else:
            return {
                'error': 'Action non reconnue',
                'status': 400
            }

        return {
            'status': 'success',
            'new_state': mail.state
        }