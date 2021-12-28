from pathlib import Path

XBEE_PORT_REQUEST = 60001
XBEE_PORT_NOTIFY = 60002
XBEE_IP_ADDRESS = '127.0.0.1'
SESSION_IDLE_TIME = 15*60
#DATABASE_URL = "sqlite:///../database/zigbee_monitor.db"
DATABASE_URL = "sqlite:///" + str(Path(__file__).parent.parent / "database" / "zigbee_monitor.db")
DEVICE_TIMEOUT = 30
STATIC_FILES_DIR = str(Path(__file__).parent / "static")

try:
    from .custom_config import *
except ImportError:
    pass