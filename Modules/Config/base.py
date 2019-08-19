# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:master20@localhost:5432/dbExperimentingTool')
Session = sessionmaker(bind=engine)

Base = declarative_base()