from models import *
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from functions.preprocess.cleanCity import cleanCity
from functions.preprocess.cleanContractType import cleanContractType
import pandas as pd

#Alimentation du DW
def fillDW(corpus):
    engine = create_engine('mysql+mysqlconnector://root:@mysql:3306/job_scrapping')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    duplicates = False
    #Vidage du DW
    session = Session()
    session.execute(text("CALL pTruncateDW()"))
    session.commit()

    i=0
    #Itération sur les éléments du corpus récupérés
    for item in corpus:
        corpus_position = item["position"]
        corpus_website = item["source"]
        corpus_link = item["link"]
        corpus_company = item["company"]
        corpus_city = cleanCity(item["workplace"])
        corpus_contract_type = cleanContractType(item["contract_type"])
        corpus_published_date = item['published_date']
        corpus_nb_occurence = item['description']
        try:
                date_object = datetime.strptime(corpus_published_date, '%d/%m/%Y')
                # If successful, use the formatted date
                corpus_published_date = date_object.strftime('%Y-%m-%d')
        except ValueError:
            corpus_published_date = datetime.now().strftime('%Y-%m-%d')
        # print(corpus_position)
        # print(corpus_position_type)
        
        # position_type = HPositionType(position_type=corpus_position_type)
        position = DPosition(position=corpus_position)
        website = DWebsite(website=corpus_website,link=corpus_link)
        company = DCompany(company=corpus_company)
        # location_infos = getLocationInfos(corpus_city)
        city = DCity(city=corpus_city)
        contract_type = DContractType(contract_type=corpus_contract_type)
        session = Session()

        # Recherche des élements de chaque dimensions pour éviter les doublons
        # existing_position_type = session.query(HPositionType).filter_by(position_type=corpus_position_type).first()
        existing_position = session.query(DPosition).filter_by(position=corpus_position).first()
        existing_website = session.query(DWebsite).filter_by(website=corpus_website).first()
        existing_company = session.query(DCompany).filter_by(company=corpus_company).first()
        existing_city = session.query(DCity).filter_by(city=corpus_city).first()
        existing_contract_type = session.query(DContractType).filter_by(contract_type=corpus_contract_type).first()

        #Si elle existe je récupère la ligne existante, sinon j'insert la nouvelle ligne
        # if existing_position_type:
            # position_type = existing_position_type
        # else:
        #     session.add(position_type)
        #     session.commit()
        if existing_position:
            position = existing_position
        else:
            session.add(position)

        if existing_website:
            website = existing_website
        else:
            session.add(website)

        if existing_company:
            company = existing_company
        else:
            session.add(company)

        if existing_city:
            city = existing_city
        else:
            session.add(city)

        if existing_contract_type:
            contract_type = existing_contract_type
        else:
            session.add(contract_type)
        session.commit()
        
        # J'insert les données dans la table de fait (id des dimensions + KPI)
        job_advertisement = FJobAdvertisements(
            nb_occurences=corpus_nb_occurence,
            position=position,
            website=website,
            company=company,
            city=city,
            contract_type=contract_type,
            published_date = corpus_published_date
        )

        session.add(job_advertisement)
        try:
            session.add(job_advertisement)
            session.commit()
            i = i + 1
        except IntegrityError as e:
            duplicates = True
            session.rollback()
        session.commit()
    session.close()
    if duplicates:
        print(f"Some exact duplicates have been detected in the job scrapping process, less documents have been saved then asked : {i} documents saved")
