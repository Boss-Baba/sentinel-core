from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("ai_brain.log"),
        logging.StreamHandler()
    ]
)

# In-memory threat log
threat_log = []

@app.route('/')
def home():
    return '<h1>🛡️ Sentinel Core AI Brain</h1><p>Status: Online</p><ul><li><a href="/health">GET /health</a></li><li><a href="/api/v1/threats">GET /api/v1/threats</a></li></ul>'

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "AI Brain online", "time": datetime.now().isoformat()})

@app.route('/api/v1/detect', methods=['POST'])
def detect_threat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data"}), 400

        threat_type = data.get("threat_type", "UNKNOWN")
        confidence = data.get("confidence", 0.0)
        action = "QUARANTINE_AND_INVESTIGATE" if threat_type == "RANSOMWARE_SIMULATION" and confidence > 0.9 else "MONITOR"

        verdict = {
            "alert_id": len(threat_log) + 1,
            "timestamp": datetime.now().isoformat(),
            "threat_type": threat_type,
            "confidence": confidence,
            "action": action
        }

        threat_log.append(verdict)
        app.logger.info(f"🚨 {action} for {threat_type} (Conf: {confidence})")

        # Forward to Response Engine
        if action == "QUARANTINE_AND_INVESTIGATE":
            try:
                import requests
                requests.post("http://localhost:9000/api/v1/response", json=verdict, timeout=5)
            except Exception as e:
                app.logger.warning(f"⚠️ Failed to notify Response Engine: {e}")

        return jsonify({"status": "ok", "verdict": verdict}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/threats', methods=['GET'])
def get_threats():
    return jsonify({"threats": threat_log[-10:]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
