from sqlalchemy import Column, Integer,String
from .base import Base

# Modele de bdd
class DCompany(Base):
    __tablename__ = 'd_company'
    id = Column(Integer, primary_key=True)
    label = Column(String)