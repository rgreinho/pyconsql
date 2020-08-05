"""Setup for the database."""
import os

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from pyconsql import connexion_utils

sql_engine = None


def get_db_settings():
    settings = connexion_utils.get_settings()
    return settings["DATABASE"]


def get_engine():
    global sql_engine
    if sql_engine:
        return sql_engine
    db_settings = get_db_settings()
    sql_engine = sqlalchemy.create_engine(db_settings["URI"], echo=True)
    return sql_engine


def get_session():
    engine = get_engine()
    return orm.scoped_session(
        orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


Base = declarative_base()
