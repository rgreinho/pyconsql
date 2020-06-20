"""Define the WSGI app."""
from pathlib import Path
from open_alchemy import init_yaml
from sqlalchemy.ext.declarative import declarative_base

from pyconsql import connexion_utils
from pyconsql import database


# Generate models.
settings = connexion_utils.get_settings()
specification_file = (
    Path(settings["BASE_DIR"]) / "openapi" / settings["SPECIFICATION_FILE"]
)
init_yaml(
    specification_file, base=database.Base, models_filename=settings["MODELS_FILENAME"],
)

# Start the API.
app = connexion_utils.create_connexion_app()
application = app.app
