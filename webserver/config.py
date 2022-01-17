# Please DO NOT modify this file. It's a default config file.
# Instead, copy the setting you want to change into custom_config.py and edit it there.

"""A module providing the configuration for the modules of the :mod:`webserver` package.

.. note::
    All the values provided in this documentation are the default values. The defaults may be overridden by the values from :mod:`~webserver.custom_config`.
    This module file should not be modified by the users. Custom values can be provided in :mod:`~webserver.custom_config`.
"""

from pathlib import Path

#: A path to the root directory of the project.
PROJECT_DIR = Path(__file__).resolve().parent.parent

#: TCP port uset for making requests to the coordinator handler.
XBEE_PORT_REQUEST = 9020

#: TCP port uset for getting notifications from the coordinator handler.
XBEE_PORT_NOTIFY = 9021

#: IP address of the coordinator handler.
XBEE_IP_ADDRESS = '127.0.0.1'

#: Time after which the user is logged out.
SESSION_IDLE_TIME = 15*60

#: Location of the SQLite database file
DATABASE_URL = "sqlite:///" + str(PROJECT_DIR / "database" / "zigbee_monitor.db")

#: Timeout for requests to the coordinator handler.
DEVICE_TIMEOUT = 30

#: The directory with static files.
STATIC_FILES_DIR = str(Path(__file__).parent / "static")

#: Configuration of the Uvicorn server.
UVICORN_CONFIG = {}

_UVICORN_CONFIG_DEFAULTS = {
    'log_config' : str(PROJECT_DIR / 'webserver' / 'uvicorn_logconfig.json')
}

try:
    from .custom_config import *
except ImportError:
    pass

UVICORN_CONFIG = {**_UVICORN_CONFIG_DEFAULTS, **UVICORN_CONFIG}
