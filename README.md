# Polymath Engineering Challenge

This project is composed of four components,

- Script for fetching categories from eBay using the trading api. Will automatically store each category in a local Sqlite database.
- Dynamic HTML rendering for on-the-fly graphical representations of our categories.
- REST api for fetching categories, includes category level filtering and by default filters expired resources.
- Frontend created with Riot.js for leveraging our REST api and viewing categories in real-time.

## Setup

The instructions express any additional modules aside from `requests` are unnecessary. Because I decided to build a full stack application, I made use of additional tools such as Flask to save time and simplify my stack.

Rather than using a standard pip requirements file, I leveraged [Pipenv](https://docs.pipenv.org/) which is a relatively new tools providing an NPM-like interface for Pypi. Pipenv is available on Windows, Mac, and Linux and can be installed with pip.

## Shell Commands

### --rebuild

Cleanup and bootstrap our database.

```bash
./server python -m polymath --rebuild
```

### --render <category_id> <to_json>

Render an HTML page based on the category provided.

```bash
./server python -m polymath --render 100100
./server python -m polymath --render 100100 1
```

## Testing

To test the backend core lib with coverage, you can leverage `pytest` installed with the dev dependencies from our Pipfile.

```bash
cd server
pipenv install && pipenv shell
pytest --cov=polymath.core tests
```

The frontend has less significant tests because I was short on time. To run the frontend tests:

```bash
cd client
npm install
npm run build
```

## Deployment

This project's frontend and backend are dockerized, and they can be deployed seemlessly.

An [ansible](https://www.ansible.com/) playbook is provided in the root directory that will automate deployment for you.

```bash
ansible-playbook deploy.yml
```

If you prefer docker compose,

```bash
docker-compose build
API_PORT=3000 docker-compose up
```

---

Copyright (c) 2018 John Nolette Licensed under the MIT license.
