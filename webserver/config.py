from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

# TCP port uset for making requests to the coordinator handler.
XBEE_PORT_REQUEST = 60001

# TCP port uset for getting notifications from the coordinator handler.
XBEE_PORT_NOTIFY = 60002

# IP address of the coordinator handler.
XBEE_IP_ADDRESS = '127.0.0.1'

# Time after which the user is logged out.
SESSION_IDLE_TIME = 15*60

# Location of the SQLite database file
DATABASE_URL = "sqlite:///" + str(PROJECT_DIR / "database" / "zigbee_monitor.db")

# Timeout for requests to the coordinator handler.
DEVICE_TIMEOUT = 30

# The directory with static files.
STATIC_FILES_DIR = str(Path(__file__).parent / "static")

# Configuration of the uvicorn server.
UVICORN_CONFIG = {}

try:
    from .custom_config import *
except ImportError:
    pass
