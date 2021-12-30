import sys
from webserver.database import SessionLocal, engine
import webserver.dbmodels as dbmodels
from webserver.pwdcontext import pwd_context
from sqlalchemy.orm import Session

def get_user_by_username(db: Session, username: str):
    return db.query(dbmodels.User).filter(dbmodels.User.username == username).first()

def create_admin(db : Session, username: str, password: str):
    password_hash = pwd_context.hash(password)
    admin = dbmodels.User(username=username, password_hash=password_hash, role='admin', disabled=False)
    db.add(admin)
    db.commit()

def change_password(db: Session, user: dbmodels.User, new_password: str):
    user.password_hash = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)

def make_admin_or_change_password(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user is None:
        create_admin(db, username, password)
        print(f'Created new admin account with username "{username}" and password "{password}"')
    else:
        change_password(db, user, password)
        print(f'Created the password of user "{username}" to "{password}"')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('The script requires two arguments: username and password.')
        exit()
    dbmodels.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    username = sys.argv[1]
    password = sys.argv[2]
    make_admin_or_change_password(db, username, password)
