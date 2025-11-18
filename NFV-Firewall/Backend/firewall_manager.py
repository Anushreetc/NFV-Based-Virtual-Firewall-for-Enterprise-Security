import sqlite3
import json
import time
from datetime import datetime
import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

class FirewallManager:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
        self.system_logs = []
        self._add_log("INFO", "Firewall Manager initialized")

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS firewalls (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                management_ip TEXT,
                subnet TEXT,
                vcpu INTEGER,
                ram INTEGER,
                security_policy TEXT,
                status TEXT,
                created_at TEXT,
                technology_stack TEXT,
                config_method TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def deploy_firewall(self, config):
        """Deploy a new firewall instance using OSM+OpenFlow"""
        firewall_id = f"fw-{int(time.time())}"
        
        try:
            self._add_log("INFO", f"Starting deployment of firewall: {config['name']}")
            
            # Step 1: Simulate OSM VNF Deployment
            self._add_log("INFO", "Step 1: Deploying VNF via OSM")
            osm_result = self._deploy_via_osm(config)
            
            # Step 2: Simulate OpenFlow Configuration
            self._add_log("INFO", "Step 2: Configuring OpenFlow rules")
            openflow_result = self._configure_openflow(firewall_id, config)
            
            # Step 3: Simulate NETCONF Configuration
            self._add_log("INFO", "Step 3: Configuring via NETCONF")
            netconf_result = self._configure_via_netconf(config)
            
            # Save to database
            self._save_firewall_to_db(firewall_id, config, "running")
            
            self._add_log("SUCCESS", f"Firewall {config['name']} deployed successfully")
            
            return {
                "success": True,
                "firewall_id": firewall_id,
                "message": "Firewall deployed successfully",
                "details": {
                    "osm": osm_result,
                    "openflow": openflow_result,
                    "netconf": netconf_result,
                    "technology_stack": "OSM + OpenFlow + NETCONF/REST"
                }
            }
            
        except Exception as e:
            self._add_log("ERROR", f"Failed to deploy firewall: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _deploy_via_osm(self, config):
        """Simulate OSM VNF deployment"""
        # In production, this would call OSM Northbound API
        vnf_config = {
            "vnfd_id": "firewall-vnfd",
            "vnf_name": config['name'],
            "vim_account": "sme-vim",
            "config": {
                "vcpu": config['vcpu'],
                "ram": config['ram'],
                "interfaces": 2
            }
        }
        
        # Simulate API call delay
        time.sleep(1)
        
        return {
            "status": "deployed",
            "vnf_id": f"vnf-{config['name']}",
            "ns_id": f"ns-{config['name']}",
            "message": "VNF instantiated successfully via OSM"
        }

    def _configure_openflow(self, firewall_id, config):
        """Simulate OpenFlow configuration"""
        # Generate flow rules based on security policy
        flow_rules = self._generate_flow_rules(config['subnet'], config['security_policy'])
        
        # In production, this would send to OpenFlow controller
        openflow_config = {
            "firewall_id": firewall_id,
            "subnet": config['subnet'],
            "policy": config['security_policy'],
            "flow_rules": flow_rules
        }
        
        time.sleep(0.5)
        
        return {
            "status": "configured",
            "rules_installed": len(flow_rules),
            "controller": Config.OPENFLOW_CONTROLLER
        }

    def _configure_via_netconf(self, config):
        """Simulate NETCONF configuration"""
        # In production, this would use ncclient to establish NETCONF session
        netconf_config = {
            "target": config['management_ip'],
            "port": Config.NETCONF_PORT,
            "username": Config.NETCONF_USERNAME,
            "config": {
                "security_policy": config['security_policy'],
                "interfaces": [
                    {"name": "eth0", "zone": "untrusted"},
                    {"name": "eth1", "zone": "trusted"}
                ]
            }
        }
        
        time.sleep(0.5)
        
        return {
            "status": "configured",
            "method": "NETCONF",
            "session_established": True
        }

    def _generate_flow_rules(self, subnet, policy):
        """Generate OpenFlow rules based on security policy"""
        rules = []
        
        if policy == "default":
            rules = [
                {"priority": 100, "action": "drop", "match": {"ipv4_src": subnet, "ip_proto": "any"}},
                {"priority": 100, "action": "drop", "match": {"ipv4_dst": subnet, "ip_proto": "any"}}
            ]
        elif policy == "web":
            rules = [
                {"priority": 200, "action": "allow", "match": {"tcp_dst": 80}},
                {"priority": 200, "action": "allow", "match": {"tcp_dst": 443}},
                {"priority": 100, "action": "drop", "match": {"ipv4_src": subnet, "ip_proto": "any"}}
            ]
        elif policy == "database":
            rules = [
                {"priority": 200, "action": "allow", "match": {"tcp_dst": 3306}},
                {"priority": 200, "action": "allow", "match": {"tcp_dst": 5432}},
                {"priority": 100, "action": "drop", "match": {"ipv4_src": subnet, "ip_proto": "any"}}
            ]
        
        return rules

    def start_firewall(self, firewall_id):
        """Start a firewall instance"""
        try:
            firewall = self._get_firewall(firewall_id)
            if not firewall:
                return {"success": False, "error": "Firewall not found"}
            
            self._add_log("INFO", f"Starting firewall: {firewall['name']}")
            
            # Simulate OSM operation
            time.sleep(1)
            
            # Update status in database
            self._update_firewall_status(firewall_id, "running")
            
            self._add_log("SUCCESS", f"Firewall {firewall['name']} started successfully")
            
            return {"success": True, "message": "Firewall started successfully"}
            
        except Exception as e:
            self._add_log("ERROR", f"Failed to start firewall: {str(e)}")
            return {"success": False, "error": str(e)}

    def stop_firewall(self, firewall_id):
        """Stop a firewall instance"""
        try:
            firewall = self._get_firewall(firewall_id)
            if not firewall:
                return {"success": False, "error": "Firewall not found"}
            
            self._add_log("INFO", f"Stopping firewall: {firewall['name']}")
            
            # Simulate OSM operation
            time.sleep(1)
            
            # Update status in database
            self._update_firewall_status(firewall_id, "stopped")
            
            self._add_log("SUCCESS", f"Firewall {firewall['name']} stopped successfully")
            
            return {"success": True, "message": "Firewall stopped successfully"}
            
        except Exception as e:
            self._add_log("ERROR", f"Failed to stop firewall: {str(e)}")
            return {"success": False, "error": str(e)}

    def configure_firewall(self, firewall_id, config):
        """Configure firewall rules"""
        try:
            firewall = self._get_firewall(firewall_id)
            if not firewall:
                return {"success": False, "error": "Firewall not found"}
            
            self._add_log("INFO", f"Configuring firewall: {firewall['name']}")
            
            # Update configuration
            if 'security_policy' in config:
                self._update_firewall_policy(firewall_id, config['security_policy'])
                self._add_log("INFO", f"Updated security policy to: {config['security_policy']}")
            
            self._add_log("SUCCESS", f"Firewall {firewall['name']} configured successfully")
            
            return {"success": True, "message": "Firewall configured successfully"}
            
        except Exception as e:
            self._add_log("ERROR", f"Failed to configure firewall: {str(e)}")
            return {"success": False, "error": str(e)}

    def delete_firewall(self, firewall_id):
        """Delete a firewall instance"""
        try:
            firewall = self._get_firewall(firewall_id)
            if not firewall:
                return {"success": False, "error": "Firewall not found"}
            
            self._add_log("INFO", f"Deleting firewall: {firewall['name']}")
            
            # Simulate OSM deletion
            time.sleep(1)
            
            # Remove from database
            self._delete_firewall_from_db(firewall_id)
            
            self._add_log("SUCCESS", f"Firewall {firewall['name']} deleted successfully")
            
            return {"success": True, "message": "Firewall deleted successfully"}
            
        except Exception as e:
            self._add_log("ERROR", f"Failed to delete firewall: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_all_firewalls(self):
        """Get all firewall instances"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM firewalls ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        firewalls = []
        for row in rows:
            firewalls.append({
                "id": row[0],
                "name": row[1],
                "management_ip": row[2],
                "subnet": row[3],
                "vcpu": row[4],
                "ram": row[5],
                "security_policy": row[6],
                "status": row[7],
                "created_at": row[8],
                "technology_stack": row[9],
                "config_method": row[10]
            })
        
        conn.close()
        return firewalls

    def get_system_logs(self):
        """Get system logs"""
        return self.system_logs[-50:]  # Return last 50 logs

    def get_statistics(self):
        """Get system statistics"""
        firewalls = self.get_all_firewalls()
        
        running = len([fw for fw in firewalls if fw['status'] == 'running'])
        stopped = len([fw for fw in firewalls if fw['status'] == 'stopped'])
        total = len(firewalls)
        
        return {
            "total_firewalls": total,
            "running_firewalls": running,
            "stopped_firewalls": stopped,
            "system_uptime": "99.8%",
            "total_logs": len(self.system_logs)
        }

    def _save_firewall_to_db(self, firewall_id, config, status):
        """Save firewall to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO firewalls 
            (id, name, management_ip, subnet, vcpu, ram, security_policy, status, created_at, technology_stack, config_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            firewall_id,
            config['name'],
            config.get('management_ip', ''),
            config.get('subnet', ''),
            config.get('vcpu', 1),
            config.get('ram', 2),
            config.get('security_policy', 'default'),
            status,
            datetime.now().isoformat(),
            "OSM+OpenFlow+NETCONF",
            config.get('config_method', 'netconf')
        ))
        
        conn.commit()
        conn.close()

    def _get_firewall(self, firewall_id):
        """Get firewall from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM firewalls WHERE id = ?', (firewall_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "management_ip": row[2],
                "subnet": row[3],
                "vcpu": row[4],
                "ram": row[5],
                "security_policy": row[6],
                "status": row[7],
                "created_at": row[8],
                "technology_stack": row[9],
                "config_method": row[10]
            }
        return None

    def _update_firewall_status(self, firewall_id, status):
        """Update firewall status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE firewalls SET status = ? WHERE id = ?', (status, firewall_id))
        conn.commit()
        conn.close()

    def _update_firewall_policy(self, firewall_id, policy):
        """Update firewall policy in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE firewalls SET security_policy = ? WHERE id = ?', (policy, firewall_id))
        conn.commit()
        conn.close()

    def _delete_firewall_from_db(self, firewall_id):
        """Delete firewall from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM firewalls WHERE id = ?', (firewall_id,))
        conn.commit()
        conn.close()

    def _add_log(self, level, message):
        """Add system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{level}] {timestamp} - {message}"
        self.system_logs.append(log_entry)
        logger.info(log_entry)