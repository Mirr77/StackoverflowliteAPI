'''import modules'''
from flask import Flask

APP = Flask(__name__)
APP.secret_key = 'secret'
APP.url_map.strict_slashes = False

from . import views
