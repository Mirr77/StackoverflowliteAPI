from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret'

from stackoverflowlite.views import views, auth, api

app.register_blueprint(api, url_prefix='/stackoverflowlite/api/v1')