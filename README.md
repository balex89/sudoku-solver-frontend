# Sudoku Solver Frontend

An HTTP web application serving user interface specifically for [this Sudoku Solver tool](https://github.com/balex89/sudoku-solver) (maintained by [@balex89](https://github.com/balex89)).

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
```commandline
pip install -r requirements.txt
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

_Mobile devices are not yet supported!_

## Sudoku grid encoding

Any time Sudoku grid is changed, it's current state is immediately encoded and put right into URL of browser address bar `/~<code>`, e.g.:

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
