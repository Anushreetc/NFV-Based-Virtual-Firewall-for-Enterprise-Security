import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OSM Configuration
    OSM_HOST = os.getenv('OSM_HOST', 'localhost')
    OSM_PORT = os.getenv('OSM_PORT', '9999')
    OSM_USERNAME = os.getenv('OSM_USERNAME', 'admin')
    OSM_PASSWORD = os.getenv('OSM_PASSWORD', 'admin')
    
    # OpenFlow Controller Configuration
    OPENFLOW_CONTROLLER = os.getenv('OPENFLOW_CONTROLLER', 'http://localhost:8080')
    
    # NETCONF Configuration (simulated)
    NETCONF_PORT = os.getenv('NETCONF_PORT', '830')
    NETCONF_USERNAME = os.getenv('NETCONF_USERNAME', 'admin')
    NETCONF_PASSWORD = os.getenv('NETCONF_PASSWORD', 'admin')
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/firewalls.db')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'sme-firewall-secret-key')