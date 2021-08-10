import logging
import requests
import json
import os

from flask import request, Response, jsonify, render_template, send_from_directory, redirect

from app.main import flask_app, config
from app.grid import Grid

SOLVER_APP_HOST = config['solverService']['host']
SOLVER_APP_PORT = config['solverService']['port']

logging.basicConfig(
    style='{',
    format='{asctime}.{msecs:03.0f} {name}:{lineno} {levelname} - {message}',
    datefmt='%Y.%m.%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def init():
    logger.info("Init app routes")


@flask_app.route("/")
@flask_app.route("/~<code>")
def home(code=None):
    try:
        grid = json.dumps(None if code is None else Grid.decode(code))
    except Exception as e:
        logger.exception('Invalid code string to decode: '
                         '"%s". Caused: %s. Redirecting to "/".', code, type(e).__name__)
        return redirect("/")
    return render_template("index.html.j2", grid=grid, version=config['app']['version'])


@flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, 'static/images'),
                               'favicon.svg', mimetype='image/svg+xml')


@flask_app.route("/solver-health", methods=["GET"])
def solver_health():
    resp = requests.request(
        method="GET",
        url=f'http://{SOLVER_APP_HOST}:{SOLVER_APP_PORT}/health',
        headers=request.headers,
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@flask_app.route("/solve", methods=["POST"])
def solve():

    resp = requests.request(
        method="POST",
        url=f'http://{SOLVER_APP_HOST}:{SOLVER_APP_PORT}/solve',
        headers=request.headers,
        data=request.get_data(),
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@flask_app.route("/encode", methods=["GET"])
def encode():
    numbers = request.args['numbers']
    return Grid.from_str(numbers).encode()


@flask_app.errorhandler(400)
def handle_bad_request(e):
    logger.exception("Bad request")
    return jsonify(status="error", error=str(e)), 400


@flask_app.errorhandler(Exception)
def handle_internal_error(e):
    logger.exception("Internal Server Error")
    return jsonify(status="error", error=str(e)), 500