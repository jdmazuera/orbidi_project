from database import Base
from sqlalchemy import Column ,JSON, String, Date, Integer, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class APICalls(Base):

    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    endpoint = Column(String)
    params = Column(JSON)
    result = Column(Text)
    