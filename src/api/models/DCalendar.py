from sqlalchemy import Column, Integer,Date
from .base import Base

# Modele de bdd
class DCalendar(Base):
    __tablename__ = 'd_calendar'
    date = Column(Date, primary_key=True)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)