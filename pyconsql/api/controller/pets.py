import logging

import connexion
from connexion import NoContent
from open_alchemy import models

from pyconsql import database

# There might be a more "SQLalchemy" way to get a session.
db_session = database.get_session()


def search(limit=100):
    # Performs the query from the session object.
    q = db_session.query(models.Pet)
    return [p.to_dict() for p in q][:limit]


def get(petId):
    # Performs the query from the model object.
    #  models.Pet.query.filter_by(id=petId).first()
    pet = db_session.query(models.Pet).filter_by(id=petId).first()
    return pet.to_dict() if pet is not None else ("Not found", 404)


def post(body):
    pet = models.Pet.from_dict(**body)
    logging.info("Creating pet %s..", pet.name)
    try:
        db_session.add(pet)
        db_session.commit()
        return NoContent, 200
    except Exception:
        db_session.rollback()
        return NoContent, 406


def delete(petId):
    logging.info("Deleting pet %s..", petId)
    # Performs the query from the model object.
    pet = models.Employee.query.filter_by(id=petId).delete()
    if pet is None:
        return NoContent, 404
    db_session.commit()
    return NoContent, 204
