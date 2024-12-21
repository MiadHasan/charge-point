from flask import Flask, jsonify, request
import asyncio
from app.charge_point import ChargePoint

app = Flask(__name__)

charge_point_instance = None  # Reference to the active ChargePoint instance


@app.route('/clear-charging-profile', methods=['POST'])
def clear_charging_profile():
    """HTTP endpoint to trigger ClearChargingProfile action."""
    data = request.json
    if not charge_point_instance:
        return jsonify({"status": "error", "message": "ChargePoint not connected"}), 400

    connector_id = data.get("connector_id")
    if connector_id is None:
        return jsonify({"status": "error", "message": "Connector ID is required"}), 400

    try:
        # Use asyncio.run to call the async clear_charging_profile method
        asyncio.run(charge_point_instance.clear_charging_profile(connector_id))
        return jsonify({"status": "ok", "message": "ClearChargingProfile request sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "hello, world"}), 200

def create_http_server(cp_instance):
    """Initialize the Flask app with the ChargePoint instance."""
    global charge_point_instance
    charge_point_instance = cp_instance
    return app
