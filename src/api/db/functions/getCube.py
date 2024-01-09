from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *
import pandas as pd
import json
from datetime import date

def serialize_dates(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    return obj

def getCube():
    engine = create_engine('mysql+mysqlconnector://root:@mysql:3306/job_scrapping')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    joined_data = (
        session.query(
            FJobAdvertisements.nb_occurences,
            DContractType.contract_type,
            DPosition.position,
            DWebsite.label.label('website'),
            DWebsite.link,
            DCity.city,
            DCompany.label.label('company'),
            DCalendar.date,
            DCalendar.day,
            DCalendar.month,
            DCalendar.year
        )
        .join(DContractType)
        .join(DPosition)
        .join(DWebsite)
        .join(DCity)
        .join(DCompany)
        .join(DCalendar)
        .all()
    )
    cube = pd.DataFrame([
        {
            'nb_occurences': row.nb_occurences,
            'contract_type': row.contract_type,
            'position': row.position,
            'website': row.website,
            'link': row.link,
            'city': row.city,
            'company': row.company,
            'published_date': row.date,
            'published_day': row.day,
            'published_month': row.month,
            'published_year': row.year,
        }
        for row in joined_data
    ])
    cube = json.dumps(cube.to_dict(orient="records"),default=serialize_dates)
    return cube