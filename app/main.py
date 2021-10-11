import configparser
import logging.config
import pathlib

import flask


def init_routes():
    from app import routes
    routes.init()


config = configparser.ConfigParser()
config.read_file(open("app/sudokuFrontend.ini", "r"))

pathlib.Path("app/logs").mkdir(exist_ok=True)
logging.config.fileConfig("app/logging.ini")

app = flask.Flask(__name__, subdomain_matching=True)
if server_name := config.get("domain", "server_name", fallback=""):
    app.config["SERVER_NAME"] = server_name

init_routes()
