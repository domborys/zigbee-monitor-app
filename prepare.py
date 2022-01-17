"""A script which configures the project.

It creates custom_config.py files, creates the SQLite database and adds first admin user.
The admin user which is created has always username "admin" and a random password which is printed into the output.

The script should be called after cloning the project from the repository. The script doesn't require any command line arguments.

.. note::
    The init.bat and init.sh both call the prepare.py, so you shouldn't call prepare.py after executing any of those scripts.
"""

import os, shutil
from pathlib import Path
from webserver.database import SessionLocal, engine
import webserver.dbmodels as dbmodels
from webserver.pwdcontext import pwd_context
from sqlalchemy.orm import Session
import secrets

#: Initial contents of receiver/custom_config.py
COORDINATOR_CUSTOM_CONFIG = """# This is a file for custom configuration.

# Serial port used for communication with the coordinator.
# Please specify the serial port, e.g. "COM3" (Windows) or "/dev/ttyUSB0" (Linux).
# The default value (None) will cause an error on startup.
DEVICE_SERIAL_PORT = None
"""

#: Initial contents of webserver/custom_config.py
WEBSERVER_CUSTOM_CONFIG = """# This is a file for custom configuration.

from .config import PROJECT_DIR 

# Configuration of the Uvicorn server.
# See https://www.uvicorn.org/settings/
# The items of UVICORN_CONFIG are passed as arguments for uvicorn.run()
UVICORN_CONFIG = dict(
    
)
"""

PROJECT_DIR = Path(__file__).resolve().parent
RECEIVER_DIR = PROJECT_DIR / 'receiver'
WEBSERVER_DIR = PROJECT_DIR / 'webserver'

def configure_custom_config(config_path : str, contents : str):
    """Creates a file with custom configuration.
    
    Args:
        config_path: path to the file to create.
        contents: initial contents of the file.
    """
    if not os.path.exists(config_path):
        with open(config_path, 'w') as web_conf:
            web_conf.write(contents)
            print(f'Created file {config_path}')
    else:
        print(f'File {config_path} already exists.')

def configure_logconfig(src_path : str, dest_path : str):
    """Copies a log config file if the destination file does not exist.
    
    Args:
        src_path: path to the file to copy. This should be the path to the existing "defaults" file.
        dest_path: path where the file should be copied.
    """
    if not os.path.exists(dest_path):
        shutil.copy(src_path, dest_path)

def create_admin(db : Session, username : str, password : str):
    """Adds an admin user into the database.
    
    Args:
        db: database session.
        username: admin's username.
        password: admin's password.
    """

    password_hash = pwd_context.hash(password)
    admin = dbmodels.User(username=username, password_hash=password_hash, role='admin', disabled=False)
    db.add(admin)
    db.commit()

def create_admin_if_not_present(db : Session):
    """Creates an admin user with username "admin" and a random password.
    if the database doesn't contain any admin user.
    
    Args:
        db: database session.
    """

    admins_count = db.query(dbmodels.User).filter(dbmodels.User.role == 'admin').count()
    if admins_count == 0:
        admin_username = 'admin'
        admin_password = secrets.token_urlsafe(8)
        create_admin(db, admin_username, admin_password)
        print(f'Created admin account with username {admin_username} and password {admin_password}')
    else:
        print('The database already has an admin user. No new admin account was created.')

if __name__ == '__main__':

    configure_custom_config(config_path=str(WEBSERVER_DIR/'custom_config.py'), contents=WEBSERVER_CUSTOM_CONFIG)
    configure_custom_config(config_path=str(RECEIVER_DIR/'custom_config.py'), contents=COORDINATOR_CUSTOM_CONFIG)
    configure_logconfig(RECEIVER_DIR/'logconfig_defaults.json', RECEIVER_DIR/'logconfig.json')
    configure_logconfig(WEBSERVER_DIR/'uvicron_logconfig_defaults.json', WEBSERVER_DIR/'uvicorn_logconfig.json')

    dbmodels.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    create_admin_if_not_present(db)
