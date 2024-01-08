from sqlalchemy import Column, Integer,String
from .base import Base

# Modele de bdd
class DWebsite(Base):
    __tablename__ = 'd_website'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    link = Column(String)