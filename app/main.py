import configparser
import logging.config
import pathlib
import logging

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

with open("app/version.txt", "r", encoding="utf8") as f:
    app.config["VERSION"] = f.read()

logger = logging.getLogger(__name__)

logger.info("Starting Sudoku-solver-frontend (%s)", app.config["VERSION"])

init_routes()
