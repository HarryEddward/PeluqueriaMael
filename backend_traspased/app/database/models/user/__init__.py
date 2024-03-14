from database.db import (
    Base,
    engine_users
)

from sqlalchemy import (
    Column,
    Integer,
    String
)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)








Base.metadata.create_all(bind=engine_users)