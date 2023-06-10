from database import Base
from sqlalchemy import Column , String , Integer, Boolean
from sqlalchemy.sql import func

class Contact(Base):

    __tablename__ = "Contact"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)
    website = Column(String)
    status_clickup = Column(Boolean)
    