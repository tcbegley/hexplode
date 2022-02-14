# Hexplode

![Lint](https://github.com/tcbegley/hexplode/workflows/Lint/badge.svg) ![Tests](https://github.com/tcbegley/hexplode/workflows/Tests/badge.svg?branch=main)

A pluggable Python implementation of a BBC Micro classic. I made this to
experiment with and learn about game playing AIs, FastAPI, WebSockets and
Svelte. Still a work in progress, I tinker around with it now and again, but it
should be pretty usable.

## Running the app

To run the app you'll need [Python 3.9+](https://www.python.org/downloads/) and
[node](https://nodejs.org/en/) installed.

Start the frontend

```sh
cd src/frontend
npm install  # only needed the first time
npm start
```

To run the backend app, use `poetry` to install the dependencies

```sh
pip install poetry
poetry install
```

then run the app with

```sh
poetry run uvicorn backend.api:app
```

The app will be available at [localhost:8080](http://127.0.0.1:8080).

## Adding bots

Custom bots should inherit from `hexplode.bot.BaseBot`, and can be added to the
app via `BOTS` and `BOT_LOOKUP` in `src/backend/api.py`.

## Running tests and linting

Tests and linters are run with `nox`

```sh
pip install nox
nox
```

`nox` will attempt to test the app for both Python 3.8 and 3.9, and hence will
fail if they aren't installed. To run tests for only 3.8 for example run

```sh
nox -s test-3.8
```
