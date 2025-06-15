from .database import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship




class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    

