import configparser
import logging.config
import pathlib

import flask


def init_routes():
    from app import routes
    routes.init()


config = configparser.ConfigParser()
config.read_file(open('app/sudokuFrontend.ini', 'r'))

pathlib.Path('app/logs').mkdir(exist_ok=True)
logging.config.fileConfig('app/logging.ini')

flask_app = flask.Flask(__name__)
init_routes()
