/ static/src/components/dispatch_tracker.js
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class DispatchTracker extends Component {
    static template = "axa_mail_tracking.DispatchTracker";

    setup() {
        this.state = useState({
            mails: [],
            isLoading: true,
            filter: 'pending'
        });

        onWillStart(async () => {
            await this.loadMails();
        });
    }

    async loadMails() {
        try {
            const result = await rpc('/api/courrier/data', {
                filter: this.state.filter
            });
            this.state.mails = result;
        } finally {
            this.state.isLoading = false;
        }
    }

    async updateStatus(mailId, action) {
        await rpc('/api/courrier/update', {
            mail_id: mailId,
            action: action
        });
        await this.loadMails();
    }
}

registry.category("public_components").add(
    "axa.DispatchTracker",
    DispatchTracker
);