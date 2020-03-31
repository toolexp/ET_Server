"""
File where information of the connection of the server with the database is configured. Mainly here is configured
the string connection with the database
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:pgTfE2020@localhost:5432/db_experimenting_tool')
Session = sessionmaker(bind=engine)

Base = declarative_base()