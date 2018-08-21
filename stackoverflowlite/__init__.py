'''import modules'''
from flask import Flask

APP = Flask(__name__)
APP.secret_key = 'secret'

from . import views
