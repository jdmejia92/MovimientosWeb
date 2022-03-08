from flask import Flask

app = Flask(__name__)

from Balance.routes import *