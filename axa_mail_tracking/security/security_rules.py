# security/security_rules.py
from odoo import models, SUPERUSER_ID


class AXASecurity(models.Model):
    _inherit = 'axa.mail.tracking'

    def _check_security(self):
        user = self.env.user
        if user.has_group('axa_mail.group_mail_manager'):
            return True
        return super()._check_security()