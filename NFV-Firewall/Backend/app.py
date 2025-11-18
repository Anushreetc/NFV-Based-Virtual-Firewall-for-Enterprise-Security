from flask import Flask, request, jsonify
from flask_cors import CORS
from firewall_manager import FirewallManager
import logging
import os

# Ensure database directory exists
os.makedirs('database', exist_ok=True)

app = Flask(__name__)
CORS(app)

# Initialize firewall manager
firewall_mgr = FirewallManager()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "SME Firewall Manager API is running",
        "version": "1.0.0",
        "technologies": ["OSM", "OpenFlow", "NETCONF", "REST API"]
    })

@app.route('/api/firewalls', methods=['GET'])
def get_firewalls():
    """Get all firewall instances"""
    try:
        firewalls = firewall_mgr.get_all_firewalls()
        return jsonify({"success": True, "firewalls": firewalls})
    except Exception as e:
        logger.error(f"Error getting firewalls: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/firewalls/deploy', methods=['POST'])
def deploy_firewall():
    """Deploy a new firewall instance"""
    try:
        config = request.json
        logger.info(f"Deploying firewall with config: {config}")
        
        # Validate required fields
        required_fields = ['name', 'management_ip', 'subnet', 'vcpu', 'ram', 'security_policy']
        for field in required_fields:
            if field not in config:
                return jsonify({
                    "success": False, 
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Deploy firewall
        result = firewall_mgr.deploy_firewall(config)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error deploying firewall: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/firewalls/<firewall_id>/start', methods=['POST'])
def start_firewall(firewall_id):
    """Start a firewall instance"""
    try:
        result = firewall_mgr.start_firewall(firewall_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error starting firewall: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/firewalls/<firewall_id>/stop', methods=['POST'])
def stop_firewall(firewall_id):
    """Stop a firewall instance"""
    try:
        result = firewall_mgr.stop_firewall(firewall_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error stopping firewall: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/firewalls/<firewall_id>/configure', methods=['POST'])
def configure_firewall(firewall_id):
    """Configure firewall rules"""
    try:
        config = request.json
        result = firewall_mgr.configure_firewall(firewall_id, config)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error configuring firewall: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/firewalls/<firewall_id>', methods=['DELETE'])
def delete_firewall(firewall_id):
    """Delete a firewall instance"""
    try:
        result = firewall_mgr.delete_firewall(firewall_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error deleting firewall: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get system logs"""
    try:
        logs = firewall_mgr.get_system_logs()
        return jsonify({"success": True, "logs": logs})
    except Exception as e:
        logger.error(f"Error getting logs: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    try:
        stats = firewall_mgr.get_statistics()
        return jsonify({"success": True, "statistics": stats})
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting SME Firewall Manager API...")
    print("Available endpoints:")
    print("  GET  /api/firewalls - List all firewalls")
    print("  POST /api/firewalls/deploy - Deploy new firewall")
    print("  POST /api/firewalls/<id>/start - Start firewall")
    print("  POST /api/firewalls/<id>/stop - Stop firewall")
    print("  GET  /api/logs - Get system logs")
    print("  GET  /api/statistics - Get statistics")
    
    app.run(host='0.0.0.0', port=5000, debug=True)