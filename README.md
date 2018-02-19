# Polymath Engineering Challenge

This project is composed of three components,

- Script for fetching categories from eBay using the trading api. Will automatically store each category in a local Sqlite database.
- Dynamic HTML rendering for on-the-fly graphical representations of our categories.
- REST api for fetching categories, includes category level filtering and by default filters expired resources.

## Setup

The instructions express any additional modules aside from `requests` are unnecessary. Because I became a little carried away and fleshed out an entire backend, I've included other modules to help simplify development.

* Flask: REST API.
* Jinja: Template preprocessor for rendering HTML.
* xml2dict: Used for converting XML into dictionaries for easier management.
* xmler: Used for converting dictionaries into XML to help better structure our requested.

Rather than using a standard pip requirements file, I leveraged [Pipenv](https://docs.pipenv.org/) which is a relatively new tool providing an NPM-like interface for Pypi. Pipenv is available on Windows, Mac, and Linux and can be installed with pip.

## Shell Commands

### --rebuild

Cleanup and bootstrap our database.

```bash
./server python -m polymath --rebuild
```

### --render <category_id>

Render an HTML page based on the category provided.

```bash
./server python -m polymath --render 100100
```

### --json <category_id>

Dump json payload for provided category.

```bash
./server python -m polymath --json 100100
```

## Testing

To test the backend core lib with coverage, you can leverage `pytest` installed with the dev dependencies from our Pipfile.

```bash
cd server
pipenv install && pipenv shell
pytest --cov=polymath.core tests
```

## Deployment

The REST api is completely dockerized, and can be built and ran without any additional overhead.

```bash
docker build . -t polymath-ebay-rest-service
docker run --rm --name polymath-rest -p 3300:33000 polymath-ebay-rest-service
```

---

Copyright (c) 2018 John Nolette Licensed under the MIT license.
