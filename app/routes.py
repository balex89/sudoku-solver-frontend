import logging
import requests
import json
import os

from flask import request, Response, jsonify, render_template, send_from_directory, redirect

from app.main import app, config
from app.grid import Grid

SOLVER_API_URL = config.get("solverService", "api_url")

if "SERVER_NAME" in app.config:
    SERVER_URL = config.get("domain", "server_url")
    SUBDOMAIN = config.get("domain", "subdomain")
    SUBDOMAIN_URL = config.get("domain", "subdomain_url") if SUBDOMAIN else SERVER_URL
else:
    SERVER_URL, SUBDOMAIN, SUBDOMAIN_URL = None, None, None

logger = logging.getLogger(__name__)


def init():
    logger.info("Init app routes")


@app.route("/static/<path:filename>", subdomain=SUBDOMAIN)
def get_static(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)


@app.route("/", subdomain=SUBDOMAIN)
@app.route("/~<code>", subdomain=SUBDOMAIN)
def sudoku(code=None):
    try:
        if code is None:
            grid, lock_mask = None, None
        else:
            grid, lock_mask = Grid.decode_locked(code)
    except Exception as e:
        logger.exception('Invalid code string to decode: '
                         '"%s". Caused: %s. Redirecting to "/".', code, type(e).__name__)
        return redirect("/")
    return render_template("index.html.j2", grid=json.dumps(grid), lock_mask=json.dumps(lock_mask),
                           version=app.config["VERSION"])


@app.route("/favicon.ico", subdomain=SUBDOMAIN)
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static/img"),
                               "favicon.svg", mimetype="image/svg+xml")


@app.route("/solver-health", methods=["GET"], subdomain=SUBDOMAIN)
def solver_health():
    resp = requests.request(
        method="GET",
        url=SOLVER_API_URL + "/health",
        headers=request.headers,
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@app.route("/solve", methods=["POST"], subdomain=SUBDOMAIN)
def solve():

    resp = requests.request(
        method="POST",
        url=SOLVER_API_URL + "/solve",
        headers=request.headers,
        data=request.get_data(),
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@app.route("/get_task", methods=["GET"], subdomain=SUBDOMAIN)  # TODO: delete
@app.route("/task", methods=["GET"], subdomain=SUBDOMAIN)
def task():
    resp = requests.request(
        method="GET",
        url=SOLVER_API_URL + "/task",
        params=request.args,
        headers=request.headers,
    )
    return Response(resp.content, resp.status_code, resp.raw.headers.items())


@app.route("/encode", methods=["GET"], subdomain=SUBDOMAIN)
def encode():
    numbers = request.args["numbers"]
    return jsonify(status="ok", code=Grid.from_str(numbers).encode_locked())


@app.route("/validate", methods=["GET"], subdomain=SUBDOMAIN)
def validate():
    numbers = request.args["numbers"]
    return jsonify(is_valid=Grid.from_str(numbers).is_valid())


@app.route("/", subdomain="<subdomain>")
@app.route("/<path:path>", subdomain="<subdomain>")
def redirect_subdomain(subdomain, path=""):
    logger.info('Redirecting %s (subdomain "%s" and path /%s) to %s',
                request.url, subdomain, path, SERVER_URL)
    return redirect(SERVER_URL)


@app.route("/")
@app.route("/<path:path>")
def home(path=""):
    logger.info("Redirecting %s%s to subdomain url %s", SERVER_URL, path, SUBDOMAIN_URL)
    return redirect(SUBDOMAIN_URL)


@app.errorhandler(400)
def handle_bad_request(e):
    logger.exception("Bad request")
    return jsonify(status="error", error=str(e)), 400


@app.errorhandler(Exception)
def handle_internal_error(e):
    logger.exception("Internal Server Error")
    return jsonify(status="error", error=str(e)), 500
