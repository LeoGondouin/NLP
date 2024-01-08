from sqlalchemy import Column, Integer,String,ForeignKey
from sqlalchemy.orm import relationship
# from .HPositionType import HPositionType

from .base import Base

# Modele de bdd
class DPosition(Base):
    __tablename__ = 'd_position'
    id = Column(Integer, primary_key=True)
    position = Column(String)