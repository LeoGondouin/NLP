from sqlalchemy import Column, Integer,String,ForeignKey,Date
from sqlalchemy.orm import relationship

from .DCalendar import DCalendar
from .DPosition import DPosition
from .DLocation import DLocation
from .DCompany import DCompany
from .DWebsite import DWebsite
from .DContractType import DContractType
from .base import Base
# Modele de bdd
class FJobAdvertisements(Base):
    __tablename__ = 'f_job_advertisements'
    nb_occurences = Column(String)
    contract_type_id = Column(Integer, ForeignKey('d_contract_type.id'),primary_key=True)
    position_id = Column(Integer, ForeignKey('d_position.id'),primary_key=True)
    website_id = Column(Integer, ForeignKey('d_website.id'),primary_key=True)
    city_id = Column(Integer, ForeignKey('d_location.id'),primary_key=True)
    company_id = Column(Integer, ForeignKey('d_company.id'),primary_key=True)
    published_date = Column(Date, ForeignKey('d_calendar.date'),primary_key=True)

    position = relationship('DPosition', back_populates='job_advertisements')
    website = relationship('DWebsite', back_populates='job_advertisements')
    company = relationship('DCompany', back_populates='job_advertisements')
    city = relationship('DLocation', back_populates='job_advertisements')
    contract_type = relationship('DContractType', back_populates='job_advertisements')

# Définition des relations
DPosition.job_advertisements = relationship('FJobAdvertisements', back_populates='position')
DWebsite.job_advertisements = relationship('FJobAdvertisements', back_populates='website')
DCompany.job_advertisements = relationship('FJobAdvertisements', back_populates='company')
DLocation.job_advertisements = relationship('FJobAdvertisements', back_populates='city')
DContractType.job_advertisements = relationship('FJobAdvertisements', back_populates='contract_type')