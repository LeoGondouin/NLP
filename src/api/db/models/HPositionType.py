from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship
from .base import Base
from .DPosition import DPosition

# Modele de bdd
class HPositionType(Base):
    __tablename__ = 'h_position_type'
    id = Column(Integer, primary_key=True)
    position_type = Column(String)