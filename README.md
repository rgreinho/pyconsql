# pyconsql

This is a simple proof of concept to show how to build a modern REST API in python.

## Abstract

This POC uses the petstore API schema as an example.

The main components are:

* [connexion](https://github.com/zalando/connexion) with
  [aiohttp](https://docs.aiohttp.org/en/stable/) as a backend
* [gunicorn](https://gunicorn.org/) with the
  [uvloop](https://github.com/MagicStack/uvloop) worker
* [OpenAlchemy](https://github.com/jdkandersson/OpenAlchemy) to generate the models on
  the fly from the specification
* [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM
* [alembic](https://alembic.sqlalchemy.org/en/latest/) to manage the migrations
* [schemathesis](https://github.com/kiwicom/schemathesis) to test our API

Other interesting libraries are:

* [loguru](https://github.com/Delgan/loguru) for better logging
* [tenacity](https://github.com/jd/tenacity) to handle retries
* [ujson](https://github.com/ultrajson/ultrajson) for ultra fast JSON processing (to be
  compared with [orjson](https://github.com/ijl/orjson) though, as ujson is slightly
  incompatible with the stdlib)

## Setup

Install the POC:

```bash
poetry install
```

Run the migrations:

```bash
make migrate
```

Start the server:

```bash
make local-api
```

## Play with it

From another terminal, you can now perform the following actions:

Populate the database:

```bash
curl -X POST "http://0.0.0.0:8000/api/pets" \
  -H "accept: application/json" \
  -d '{"name": "tiger", "tag": "wild"}'
curl -X POST "http://0.0.0.0:8000/api/pets" \
  -H "accept: application/json" \
  -d '{"name": "molly", "tag": "homebuddy"}'
```

Retrieve all the pets:

```bash
curl -s -X GET "http://0.0.0.0:8000/api/pets" -H "accept: application/json" | jq
```

Retrieve a specific pet:

```bash
curl -s -X GET "http://0.0.0.0:8000/api/pets/1" -H "accept: application/json" | jq
```

## Test it

```bash
poetry run schemathesis run http://0.0.0.0:8000/api/openapi.json
```

The endpoint `POST /api/pets` fails because there is no valid example associated to it
in the specification file.

## Clean up

Destroy the DB and associated migrations:

```bash
make cleanup
```

## What's needed to make it production ready

* Improve the configuration system
  * Parameters should have sensible default values
  * All the parameters that can be inferred or calculated should be inferred or calculated (i.e. the specfile path)
* Remove GUnicorn
  * Although it does not bring much overhead, it is not needed by modern application frameworks and the scaling/healthcheck/restart will be handled by kubernetes
* Use ultra fast libraries
  * Replace the default event loop with UVLoop
* Replace the Makefile with [Invoke](https://www.pyinvoke.org/) tasks
* Create a nice template
  * Cookiecutter (?)
  * Only the name of the app should be required

## Can I push it even further?

It starts to get hard to obtain better performance using Python, but here are some pointers to push asyncio to its limits:

* Use [async](https://github.com/MagicStack/asyncpg) to handle PostgreSQL.
  * It only works with [SQL Alchemy Core](https://docs.sqlalchemy.org/en/13/core/) though, therefore there may be some adjutsments to make to still be able to use Open Alchemy.
* Use the [aio-libs](https://github.com/aio-libs) whenever possible.
* Check the [aiohttp extensions](https://docs.aiohttp.org/en/stable/third_party.html#aiohttp-extensions).

## I still need more

Use Go or Rust!
