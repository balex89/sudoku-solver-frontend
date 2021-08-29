# Sudoku Solver Frontend

An HTTP web application serving user interface specifically for [this Sudoku Solver tool](https://github.com/balex89/sudoku-solver) (maintained by [@balex89](https://github.com/balex89)). Solver service API v1 is used.


Provides a user with a [Sudoku](https://en.wikipedia.org/wiki/Sudoku) grid to fill in, and a button to show the solution in place.
Works with [basic puzzle rules](https://www.learn-sudoku.com/sudoku-rules.html).

Featuring immediate URL-safe [grid encoding](#sudoku-grid-encoding).

<p align="center">
  <img src="img/example.png" width="500">
</p>

## Prerequisites
- [Python 3.9 +](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

## Setup

### Install dependencies:
```commandline
pip install -r requirements.txt
```

### Configuration:
Config file `sudokuFrontend.ini` provides some customization options:

#### Solver service socket
Is specified in `[solverService]` section. E.g. to run on the same host:
```ini
[solverService]
host = localhost
port = 5000
; ... leave other keys intact
```

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

## Run tests
```commandline
python -m pytest -v
```

## Run web-server
On Windows (e.g. on port 5001):
```
set FLASK_APP=app.main
python -m flask run -h 0.0.0.0 -p 5001
```

## Browser and resolution capability
Works well on desktop browsers:
- [Google Chrome](https://www.google.com/intl/en_en/chrome/) (_tested on v92.0.4515_)
- [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/) (_tested on v90.0.2_)
- [Microsoft Edge](https://www.microsoft.com/en-US/edge) (_tested on v44.17763.1_)

Best in 640 x 910 resolution or higher.

_Mobile devices are poorly supported._

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

Feel free to contact: [balex89@gmail.com](mailto:balex89@gmail.com).
