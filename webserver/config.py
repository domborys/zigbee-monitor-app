XBEE_PORT_REQUEST = 60001
XBEE_PORT_NOTIFY = 60002
XBEE_IP_ADDRESS = '127.0.0.1'
SESSION_IDLE_TIME = 15*60
DATABASE_URL = "sqlite:///../database/zigbee_monitor.db"

try:
    from custom_config import *
except ImportError:
    pass