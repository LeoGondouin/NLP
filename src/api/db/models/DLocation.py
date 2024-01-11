from sqlalchemy import Column, Integer,String
from .base import Base

# Modele de bdd
class DLocation(Base):
    __tablename__ = 'd_location'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    city_coords = Column(String)
    department = Column(String)
    department_coords = Column(String)
    region = Column(String)
    region_coords = Column(String)