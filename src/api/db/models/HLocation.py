from sqlalchemy import Column, Integer,String,Double,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

# Modele de bdd
class HLocation(Base):
    __tablename__ = 'h_ref_location'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    department = Column(String)
    region = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
