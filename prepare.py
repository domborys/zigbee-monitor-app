import os
from webserver.database import SessionLocal, engine
import webserver.dbmodels as dbmodels
from webserver.pwdcontext import pwd_context
from sqlalchemy.orm import Session
import secrets

def configure_custom_config(config_path, contents):
    if not os.path.exists(config_path):
        with open(config_path, 'w') as web_conf:
            web_conf.write(contents)
            print(f'Created file {config_path}')
    else:
        print(f'File {config_path} already exists.')

def create_admin(db : Session, username, password):
    password_hash = pwd_context.hash(password)
    admin = dbmodels.User(username=username, password_hash=password_hash, role='admin', disabled=False)
    db.add(admin)
    db.commit()

def create_admin_if_not_present(db : Session):
    admins_count = db.query(dbmodels.User).filter(dbmodels.User.role == 'admin').count()
    if admins_count == 0:
        admin_username = 'admin'
        admin_password = secrets.token_urlsafe(8)
        create_admin(db, admin_username, admin_password)
        print(f'Created admin account with username {admin_username} and password {admin_password}')
    else:
        print('The database already has an admin user. No new admin account was created.')

if __name__ == '__main__':
    configure_custom_config(config_path='webserver/custom_config.py', contents='# This is a file for custom configuration')
    configure_custom_config(config_path='receiver/custom_config.py', contents='# This is a file for custom configuration')

    dbmodels.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    create_admin_if_not_present(db)
