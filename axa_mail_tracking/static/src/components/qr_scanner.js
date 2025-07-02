/** @odoo-module **/
import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class QRScanner extends Component {
    static template = "axa_mail_tracking.QRScanner";
    static props = ['onScan', 'title'];

    setup() {
        this.state = useState({
            isScanning: false,
            error: null
        });
        this.videoRef = { current: null };
        this.mediaStream = null;
        this.scannerInterval = null;
        this.notification = useService("notification");
    }

    async startScanner() {
        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            this.videoRef.current.srcObject = this.mediaStream;
            this.state.isScanning = true;
            this.scannerInterval = setInterval(() => this.detectQR(), 500);
        } catch (error) {
            this.state.error = _t("Erreur caméra: ") + error.message;
            this.notification.add(this.state.error, { type: 'danger' });
        }
    }

    detectQR() {
        // Intégration avec jsQR library
        const video = this.videoRef.current;
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

            // Détection QR (implémentation réelle nécessite jsQR)
            const fakeQRDetection = "AXA-COURRIER-0001";
            if (fakeQRDetection) {
                this.props.onScan(fakeQRDetection);
                this.stopScanner();
            }
        }
    }

    stopScanner() {
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
        }
        if (this.scannerInterval) {
            clearInterval(this.scannerInterval);
        }
        this.state.isScanning = false;
    }

    onWillUnmount() {
        this.stopScanner();
    }
}

registry.category("public_components").add("axa.QRScanner", QRScanner);