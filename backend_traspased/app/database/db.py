from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


DEV_DB_STAFF = "sqlite:///test_staff.db"
DEV_DB_USERS = "sqlite:///test_users.db"

PRO_DB_STAFF = "mysql+pymysql://root:Dark_Draw_Everything@localhost/peluqueria_mael_adminstaff?charset=utf8mb4"
PRO_DB_USERS = "mysql+pymysql://root:Dark_Draw_Everything@localhost/peluqueria_mael_users?charset=utf8mb4"


#START ENGINE USERS

engine_users = create_engine(DEV_DB_USERS)
SessionLocalUsers = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_users
)

#END ENGINE USERS




#START ENGINE STAFF

engine_staff = create_engine(DEV_DB_STAFF)
SessionLocalStaff = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_staff
)

#END ENGINE STAFF


Base = declarative_base()




#START! Instancias de diferentes db

def get_db_staff():
    db = SessionLocalStaff()
    try:
        yield db
    finally:
        db.close()

def get_db_users():
    db = SessionLocalUsers()
    try:
        yield db
    finally:
        db.close()

#END! Instancias de diferentes db
