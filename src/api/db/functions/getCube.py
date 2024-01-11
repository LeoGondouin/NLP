from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,text
from models import *
import pandas as pd
import json
from datetime import date
import calendar

def serialize_dates(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    return obj

def getCube(filter_criterias):
    engine = create_engine('mysql+mysqlconnector://root:@mysql:3306/job_scrapping')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    joined_data = (
        session.query(
            FJobAdvertisements.nb_occurences,
            DContractType.contract_type,
            DPosition.position,
            DWebsite.website,
            DWebsite.link,
            DLocation.city,
            DLocation.city_coords,
            DCompany.company,
            DCalendar.date,
            DCalendar.day,
            DCalendar.month,
            DCalendar.year
        )
        .join(DContractType)
        .join(DPosition)
        .join(DWebsite)
        .join(DLocation)
        .join(DCompany)
        .join(DCalendar)      
        .filter(
            text(filter_criterias)
        )
        .all()
    )

    cube = pd.DataFrame([
        {
            'nb_occurences': row.nb_occurences,
            'contract_type': row.contract_type,
            'position': row.position,
            'website': row.website,
            'link': row.link,
            'city': row.city.lower().capitalize(),
            'company': row.company,
            'published_date': row.date,
            'published_day': row.day,
            'published_month_int': row.month,
            'published_month': calendar.month_name[row.month],
            'published_year': row.year,
            'coords': row.city_coords,
        }
        for row in joined_data
    ])
    cube = json.dumps(cube.to_dict(orient="records"),default=serialize_dates)
    return cube