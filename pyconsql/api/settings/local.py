"""Define the connexion settings for a local setup."""
import os

# pylint: disable=wildcard-import,unused-wildcard-import
from pyconsql.api.settings.common import *  # noqa

DEBUG = True
if os.environ.get("KUBERNETES_PORT"):
    minikube_ip = os.environ.get("MINIKUBE_IP", "192.168.99.100")
    BASE_URL = f"http://api.{minikube_ip}.nip.io"
else:
    environment_based_spec_dir = "openapi"
    BASE_URL = f"http://0.0.0.0:{PORT}"  # noqa: F405
    SPECIFICATION_DIR = os.path.join(BASE_DIR, environment_based_spec_dir)  # noqa: F405

DATABASE = {
    "URI": "sqlite:///petstore.db",
}
