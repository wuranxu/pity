from flask import Flask

from config import Config

pity = Flask(__name__)


pity.config.from_object(Config)
