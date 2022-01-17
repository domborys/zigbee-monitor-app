"""A scripts which can be used to create a new admin or to change the password of a user.

The script requires two command-line arguments: `username` and `password`.
If the user with the given `username` exists in the database then their password is changed to `password`.
If there is no user with the `username` a new admin user is created.
"""
import sys
from typing import Optional
from webserver.database import SessionLocal, engine
import webserver.dbmodels as dbmodels
from webserver.pwdcontext import pwd_context
from sqlalchemy.orm import Session

def get_user_by_username(db: Session, username: str) -> Optional[dbmodels.User]:
    """Finds a user in the database by username.
    
    Args:
        db: database session
        username: user's username
        
    Returns:
        The user with the specified username or None if no user has such a username."""
    return db.query(dbmodels.User).filter(dbmodels.User.username == username).first()

def create_admin(db : Session, username: str, password: str):
    """Creates an admin user.
    
    Args:
        db: database session
        username: admin's username
        password: admin's password
    """
    password_hash = pwd_context.hash(password)
    admin = dbmodels.User(username=username, password_hash=password_hash, role='admin', disabled=False)
    db.add(admin)
    db.commit()

def change_password(db: Session, user: dbmodels.User, new_password: str):
    """Creates user's password.
    
    Args:
        db: database session
        user: user whose password will be changed.
        new_password: new password of the user.
    """

    user.password_hash = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)

def make_admin_or_change_password(db: Session, username: str, password: str):
    """Creates an admin user if there is no user with the given `username`
    or changes the password of the user if the user exists in the database.
    
    Args:
        db: database session
        username: user's username
        password: user's password
    """
    user = get_user_by_username(db, username)
    if user is None:
        create_admin(db, username, password)
        print(f'Created new admin account with username "{username}" and password "{password}"')
    else:
        change_password(db, user, password)
        print(f'Changed the password of user "{username}" to "{password}"')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('The script requires two arguments: username and password.')
        exit()
    dbmodels.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    username = sys.argv[1]
    password = sys.argv[2]
    make_admin_or_change_password(db, username, password)
