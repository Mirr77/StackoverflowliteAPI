from flask import Flask
from db import create_tables

create_tables.create_tables()
app = Flask(__name__)
app.url_map.strict_slashes = False

from stackoverflowlite.views import questions, auth, api

app.register_blueprint(api, url_prefix='/api/v1')