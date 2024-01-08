from sqlalchemy import Column, Integer,String,ForeignKey
from .base import Base

# Modele de bdd
class DContractType(Base):
    __tablename__ = 'd_contract_type'
    id = Column(Integer, primary_key=True)
    contract_type = Column(String)