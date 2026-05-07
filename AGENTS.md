# AGENTS.md

## Overview

This repository runs a Docker Compose stack that combines Django authentication, Nginx routing, MariaDB, and two Shiny Server runtimes for different R versions.

- Start from [README.md](README.md) for environment bootstrap and deployment steps.
- The stack definition is in [docker-compose.yml](docker-compose.yml).
- Django code lives in [django-data/shiny](django-data/shiny).
- Nginx auth and proxy rules live in [nginx-conf.d/nginx-default.conf](nginx-conf.d/nginx-default.conf).
- Shiny server configuration lives in [shiny/shiny-server.conf](shiny/shiny-server.conf).
- R applications live in [shiny-apps](shiny-apps).

## Working Rules

- Run project commands from the repository root.
- Prefer targeted changes. Do not modify [mysql-data](mysql-data) or [renv-cache](renv-cache) unless the task is explicitly about local data or R package cache state.
- Link to existing docs instead of duplicating them. The repo-level README is the primary human-facing setup guide.
- Keep changes consistent with the current split between Django auth logic, Nginx routing, and Shiny apps.

## Architecture

- `nginx` is the public entrypoint and proxies Django plus both Shiny runtimes; see [nginx-conf.d/nginx-default.conf](nginx-conf.d/nginx-default.conf).
- `uwsgi` serves the Django project from [django-data/shiny](django-data/shiny) using settings in [django-data/shiny/shiny/settings.py](django-data/shiny/shiny/settings.py).
- `db` is MariaDB initialized by [docker-entrypoint-initdb.d/01-create_database.sh](docker-entrypoint-initdb.d/01-create_database.sh).
- `shiny-4.0` and `shiny-4.5` both mount [shiny-apps](shiny-apps), and app URLs are version-prefixed.

## Django Conventions

- The main app is [serve](django-data/shiny/serve) and the core model is [django-data/shiny/serve/models.py](django-data/shiny/serve/models.py).
- `ShinyApp.location` must start with `/shiny-{r_version}/`; this is validated in the model and is part of the routing contract.
- Access control is enforced in two places and changes usually need to stay aligned:
  - page rendering in [django-data/shiny/serve/views.py](django-data/shiny/serve/views.py)
  - Nginx subrequest authorization in the `auth` view in [django-data/shiny/serve/views.py](django-data/shiny/serve/views.py)
- URL patterns are defined in [django-data/shiny/shiny/urls.py](django-data/shiny/shiny/urls.py).
- Django dependencies and formatter/linter settings are in [uwsgi/pyproject.toml](uwsgi/pyproject.toml).

## Commands Agents Should Prefer

The safest way to run project code is through Docker Compose because Django expects MariaDB service names and env vars from `.env`.

- Start stack: `docker compose up -d`
- Build images: `docker compose build`
- Run Django checks: `docker compose run --rm -u $(id -u):www-data uwsgi python manage.py check`
- Run migrations: `docker compose run --rm -u $(id -u):www-data uwsgi python manage.py migrate`
- Run tests: `docker compose run --rm -u $(id -u):www-data uwsgi pytest`

If the task is limited to Python formatting or static analysis, inspect [uwsgi/pyproject.toml](uwsgi/pyproject.toml) before introducing new tooling.

## Environment Pitfalls

- A local `.env` file is required for most runtime commands; see [README.md](README.md).
- Permissions on [django-data/shiny/media](django-data/shiny/media) and thumbnails commonly need fixing after setup; follow the commands in [README.md](README.md).
- R package behavior depends on the mounted [renv-cache](renv-cache) and the app files in [shiny-apps](shiny-apps).
- Nginx forwards the original URI through `X-Original-URI`; changes to auth or routing should be checked against [nginx-conf.d/nginx-default.conf](nginx-conf.d/nginx-default.conf) and [django-data/shiny/serve/views.py](django-data/shiny/serve/views.py).

## When Extending Instructions

Create more specific instruction files only if repeated work emerges in one of these areas:

- Django model/view changes under [django-data/shiny/serve](django-data/shiny/serve)
- container or proxy changes under [docker-compose.yml](docker-compose.yml), [nginx-conf.d](nginx-conf.d), or [shiny](shiny)
- Shiny app authoring conventions under [shiny-apps](shiny-apps)
