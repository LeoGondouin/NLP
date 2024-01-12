from sqlalchemy import Column, Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

# Modele de bdd
class DCity(Base):
    __tablename__ = 'd_city'
    id = Column(Integer, primary_key=True)
    city_ref_location_id = Column(Integer)
    city = Column(String)