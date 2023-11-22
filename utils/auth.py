# Imports
import dash_auth
from ..settings import producao
from app import app

# Authentication
if producao:
    dash_username = open("/run/secrets/dash_username").read().strip()
    dash_password = open("/run/secrets/dash_password").read().strip()
    auth = dash_auth.BasicAuth(app, {dash_username: dash_password})