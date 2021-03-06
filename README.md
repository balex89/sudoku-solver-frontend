# Sudoku Solver Frontend by [Kalinbob](http://kalinbob.com)

An HTTP web application serving user interface specifically for [this Sudoku Solver tool](https://github.com/balex89/sudoku-solver) (maintained by [@balex89](https://github.com/balex89)). Solver service API v1 is used.

Try it now at [sudoku.kalinbob.com](http://sudoku.kalinbob.com)! 

The app provides a user with a [Sudoku](https://en.wikipedia.org/wiki/Sudoku) grid to fill in (manually or automatically by puzzle generator), tools to solve, unsolve, clear grid or undo recent changes.
Works with [basic puzzle rules](https://www.learn-sudoku.com/sudoku-rules.html). Highlights cells that violate puzzle rules, if any.

Featuring immediate URL-safe [grid encoding](#sudoku-grid-encoding).

<p align="center">
  <img src="img/example.png" width="500">
</p>

## Prerequisites
- [Docker 20.10+](https://docs.docker.com/engine/install/) (_for amd64 linux platform only_)

or 

- [Python 3.9 +](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

## Docker setup and run
Pull the latest build available:
```shell
docker pull kalinbob/sudoku-solver-frontend:latest
```
Or one of stable [release versions available](https://hub.docker.com/repository/docker/kalinbob/sudoku-solver-frontend) (see [release notes](https://github.com/balex89/sudoku-solver/releases) for details).

Run pulled `<VERSION>` on `<PORT>` of your choice. Provide [`<CONFIG>`](#configuration) file path:
```shell
docker run --name=sudoku-solver -d -p <PORT>:5001 -v <CONFIG>:/app/sudokuFrontend.ini:ro kalinbob/sudoku-solver-frontend:<VERSION>
```
Add this option for writing logs to`<DIRECTORY>` on the host:
```shell
-v <DIRECTORY>:/app/logs
```

### Configuration:
Config file [`app/sudokuFrontend.ini`](app/sudokuFrontend.ini) provides some customization options:

#### Solver service socket
Is specified in `[solverService]` section. E.g. to run on the same host:
```ini
[solverService]
host = localhost
port = 5000
; ... leave other keys intact
```
_**Note when using Docker**: container by default treats `localhost` as itself, **not** the Docker host. Consider using [`--network host` option](https://docs.docker.com/network/network-tutorial-host/) or other ways of referring to host._
#### Subdomain redirecting
_Note: for complex URL forwarding consider using specialized solutions like [Nginx](https://nginx.org/) or [Apache HTTP Server](https://httpd.apache.org/)._

In case you run app on a domain (e.g. `example.com`) and want to redirect there any request with inappropriate url like this:
```
http://www.example.com/
http://any_subdomain.example.com/any/path
http://example.com/any/unmatched/path
```
then provide `server_name` to `[domain]` section:
```ini
[domain]
server_name = example.com:80
subdomain =
; ... leave other keys intact
```
In case you want to run app on a specific subdomain (e.g. `app.example.com`) and set redirection for urls like:
```
http://example.com/
http://example.com/any/path
http://app.example.com/any/unmatched/path
http://any_other_subdomain.example.com/any/path
```
then additionally provide `subdomain`:
```ini
[domain]
server_name = example.com:80
subdomain = app
; ... leave other keys intact
```
To test this feature locally append domain records to [`hosts` file](https://en.wikipedia.org/wiki/Hosts_(file)):
```
127.0.0.1 example.com
127.0.0.1 app.example.com
127.0.0.1 any_other_subdomain.example.com
```

## Classic setup, test and run

### Install dependencies:
```shell
pip install -r requirements.txt
```

### Run tests
```shell
python -m pytest -v
```

### Run web-server
On Windows (e.g. on port 5001):
```shell
set FLASK_APP=app.main
python -m flask run -h 0.0.0.0 -p 5001
```

## Browser and resolution capability
Works well on desktop browsers:
- [Google Chrome](https://www.google.com/intl/en_en/chrome/) (_tested on v92.0.4515_)
- [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/) (_tested on v90.0.2_)
- [Microsoft Edge](https://www.microsoft.com/en-US/edge) (_tested on v44.17763.1_)

Best in 640 x 910 resolution or higher.

_Most up-to-date mobile devices should be well-supported. Please report bugs and usability suggestions to [team@kalinbob.com](mailto:team@kalinbob.com)._

## Sudoku grid encoding

Any time Sudoku grid is changed, it's current state is immediately encoded and put right into URL of browser address bar (`.../~<code>`), e.g.:

```
http://localhost:5001/~hFEB_iAwZIFzybz14z-gDafDf4tRy
```

One can share or save this link for future to reconstruct current state of grid. Code can be used even on other instances of application. 

If you are interested in encoder implementation, see [grid.py module](app/grid.py).

## Status
Work in progress.

## Contributors and Contacts
Aka Kalinbob team:
- [@KalinovSergey](https://github.com/KalinovSergey)
- [@belnast5](https://github.com/belnast5)
- [@balex89](https://github.com/balex89) (_Lead maintainer_)

Feel free to contact: [team@kalinbob.com](mailto:team@kalinbob.com).
