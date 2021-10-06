import logging
import requests
import json
import os

from flask import request, Response, jsonify, render_template, send_from_directory, redirect

from app.main import app, config
from app.grid import Grid

SOLVER_API_URL = config["solverService"]["api_url"]

logger = logging.getLogger(__name__)


def init():
    logger.info("Init app routes")


@app.route("/")
@app.route("/~<code>")
def home(code=None):
    try:
        grid = json.dumps(None if code is None else Grid.decode(code))
    except Exception as e:
        logger.exception('Invalid code string to decode: '
                         '"%s". Caused: %s. Redirecting to "/".', code, type(e).__name__)
        return redirect("/")
    return render_template("index.html.j2", grid=grid, version=config["app"]["version"])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static/img"),
                               "favicon.svg", mimetype="image/svg+xml")


@app.route("/solver-health", methods=["GET"])
def solver_health():
    resp = requests.request(
        method="GET",
        url=SOLVER_API_URL + "/health",
        headers=request.headers,
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@app.route("/solve", methods=["POST"])
def solve():

    resp = requests.request(
        method="POST",
        url=SOLVER_API_URL + "/solve",
        headers=request.headers,
        data=request.get_data(),
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@app.route("/encode", methods=["GET"])
def encode():
    numbers = request.args["numbers"]
    return Grid.from_str(numbers).encode()


@app.route("/validate", methods=["GET"])
def validate_mock():
    return jsonify(is_valid=True)


@app.errorhandler(400)
def handle_bad_request(e):
    logger.exception("Bad request")
    return jsonify(status="error", error=str(e)), 400


@app.errorhandler(Exception)
def handle_internal_error(e):
    logger.exception("Internal Server Error")
    return jsonify(status="error", error=str(e)), 500
