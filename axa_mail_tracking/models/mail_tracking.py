from odoo import models, fields, api, _
import qrcode
import base64
from io import BytesIO
from odoo.exceptions import UserError


class AXAMailTracking(models.Model):
    _name = 'axa.mail.tracking'
    _description = 'Suivi des Courriers Entrants AXA'

    name = fields.Char("Référence", default="Nouveau", readonly=True)
    mail_type = fields.Selection([
        ('sinistre', 'Sinistre'),
        ('reclamation', 'Réclamation'),
        ('souscription', 'Souscription'),
        ('resiliation', 'Résiliation')
    ], string="Type de courrier", required=True)
    sender = fields.Char("Expéditeur", tracking=True)
    recipient_id = fields.Many2one('res.users', "Direction Destinataire")
    date_received = fields.Datetime("Date de réception", default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'À recevoir'),
        ('received', 'Reçu'),
        ('rejected', 'Rejeté'),
        ('dispatched', 'Distribué'),
        ('done', 'Traité')
    ], string="État", default='draft')
    qr_code = fields.Binary("QR Code", attachment=True, compute='_generate_qr_code', store=True)
    qr_content = fields.Char("Contenu QR", compute='_generate_qr_content', store=True)
    dispatch_history = fields.One2many('axa.dispatch.history', 'mail_id', "Historique")
    attachment = fields.Binary("Document scanné")
    rejection_reason = fields.Text("Motif de rejet")

    @api.depends('name')
    def _generate_qr_content(self):
        for record in self:
            record.qr_content = f"AXA-COURRIER-{record.name}"

    @api.depends('name')
    def _generate_qr_code(self):
        for record in self:
            if record.name:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(record.qr_content)
                qr.make(fit=True)
                img = qr.make_image()
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                record.qr_code = base64.b64encode(buffer.getvalue())

    def action_validate(self):
        self.write({'state': 'received'})
        self._create_history("Validation", "Courrier validé")

    def action_reject(self):
        return {
            'name': _('Rejet du courrier'),
            'type': 'ir.actions.act_window',
            'res_model': 'mail.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mail_id': self.id},
        }

    def action_dispatch(self):
        self.write({'state': 'dispatched'})
        self._create_history("Distribution", "En cours de distribution")

    def _create_history(self, action, notes):
        self.env['axa.dispatch.history'].create({
            'mail_id': self.id,
            'user_id': self.env.user.id,
            'action': action,
            'notes': notes
        })


class DispatchHistory(models.Model):
    _name = 'axa.dispatch.history'
    _description = 'Historique de Distribution'

    mail_id = fields.Many2one('axa.mail.tracking', "Courrier", ondelete='cascade')
    user_id = fields.Many2one('res.users', "Utilisateur")
    timestamp = fields.Datetime("Date/Heure", default=fields.Datetime.now)
    action = fields.Char("Action")
    notes = fields.Text("Notes")