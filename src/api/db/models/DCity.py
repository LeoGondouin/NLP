from sqlalchemy import Column, Integer,String
from .base import Base

# Modele de bdd
class DCity(Base):
    __tablename__ = 'd_city'
    id = Column(Integer, primary_key=True)
    city = Column(String)