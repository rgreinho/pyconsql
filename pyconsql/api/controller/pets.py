import connexion
from connexion import NoContent

from pyconsql import database
from pyconsql.api.model.pet import Pet

db_session = database.get_session()


def search(limit=100, animal_type=None):
    q = db_session.query(Pet)
    if animal_type:
        q = q.filter(Pet.animal_type == animal_type)
    return [p.dump() for p in q][:limit]


def get(pet_id):
    pet = db_session.query(Pet).filter(Pet.id == pet_id).one_or_none()
    return pet.dump() if pet is not None else ("Not found", 404)


def post(pet):
    logging.info("Creating pet %s..", pet_id)
    pet["created"] = datetime.datetime.utcnow()
    db_session.add(Pet(**pet))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete(pet_id):
    pet = db_session.query(Pet).filter(Pet.id == pet_id).one_or_none()
    if pet is not None:
        logging.info("Deleting pet %s..", pet_id)
        db_session.query(Pet).filter(Pet.id == pet_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404
