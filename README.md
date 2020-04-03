
Shiny-django authentication
===========================

This is an attempt of managing shiny authentication with django starting from this
[guide](http://pawamoy.github.io/2018/03/15/django-auth-server-for-shiny/) and
modifying stuff accordingly. The django template derive from
[this repository](https://github.com/cnr-ibba/dockerfiles/tree/master/compose/django)
while the shiny specific configuration comes from [here](https://github.com/cnr-ibba/dockerfiles/tree/master/compose/shiny)
The aim of this project is to provide both free and restricted access to shiny
applications relying on django authentication system and nginx. Applications could
be accessed using the django frontend as a container of iframe application or
directly by specifying the path of the application. A specific NGINX configuration
will be responsible to provide access to shiny applications relying on django
authentication system.

Install docker and docker-compose
---------------------------------

All this stuff works inside a docker compose image and need [docker](https://www.docker.com/)
and [docker-compose](https://docs.docker.com/compose/) to work. Please refer to
the official documentation on how to install [docker](https://docs.docker.com/install/)
and [docker-compose](https://docs.docker.com/compose/install/)

The shiny-server composed image
-------------------------------

The `shiny-server` project is composed by four different docker images:
- `db`: a MySQL database which stores information about users credentials
- `shiny`: a `rocker/shiny` based images with few dependencies installed to render
  shiny applications
- `uwsgi`: a Django base image which implements views and authentication system
- `nginx`: used as a proxy to connect `shiny` and `uwsgi` backends. A special
  configuration location lets to provide shiny contents to authenticated users

### Setting up the environment file

`docker-compose` can read variables from a `.env` placed in the working directory.
Here we will define all variables useful for our containers, like database password.
Edit a new `.env` file in working directory and set passwords for such environment
variables:

```
MYSQL_ROOT_PASSWORD=<root_password>
SHINY_DATABASE=<shiny_db>
SHINY_USER=<shiny_user>
SHINY_PASSWORD=<shiny_password>
```

> *TODO*: manage sensitive data using secret in docker-compose, as described
[here](https://docs.docker.com/engine/swarm/secrets/#use-secrets-in-compose) and
[here](https://docs.docker.com/compose/compose-file/#secrets)

### Preparing the database

All information needed to instantiate database (like tables, password, user) are
defined in `docker-entrypoint-initdb.d` directory. Database will be generated and then all the scripts
placed in `docker-entrypoint-initdb.d` directory are executed. Ensure that `mysql-data` is not present,
if not this part of the configuration will not be executed.

> NOTE:
the entire system (three containers managed by Docker Compose) uses two shared
[volumes](https://docs.docker.com/engine/admin/volumes/volumes/) for ensuring
the existance of persistent data: on the host the two directories are named
`mysql-data/` and `django-data/`. The django-data directory, containing the
entire django environment and codes, is tracked in git while `mysql-data` not.
When instantiated for the first time, `mysql-data` is generated and the database
is initialized. After that, every instance of mysql will use the `mysql-data`
directory, mantaing already generate data. If you plan to move `shiny-server`,
you have to move all `shiny-server` directory with all its content

### Build the docker-compose suite

In order to build the images according to the docker-compose.yml specificatios,
Docker will download and install all required dependencies; it will need several
minutes to complete. Launch this command from the working directory:

```
$ docker-compose build
```

### Django configuration

Django configuration relies on a `settings.py` module, which loads sensitive data
like password and `SECRET_KEY` from the same `.env` file in the project directory
through the [python decouple](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html)
module. You need to define new environment variables for `uwsgi` container:

You need to define a new django `SECRET_KEY`. Start a python terminal with docker:

```
$ docker-compose run --rm --no-deps uwsgi python
```
then execute this python code, as described [here](https://stackoverflow.com/a/16630719):

```python
>>> from django.utils.crypto import get_random_string
>>> chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
>>> get_random_string(50, chars)
```

Copy the resulting key and the add into the previous `.env` file like this:

```
SECRET_KEY=<your SECRET_KEY>
DEBUG=False
```

### Fixing django permissions

You will also to check file permissions in django data, expecially for `media`
folder:

```
$ docker-compose run --rm uwsgi sh -c 'mkdir -p /var/uwsgi/shiny/media'
$ docker-compose run --rm uwsgi sh -c 'chmod -R g+rw media'
$ docker-compose run --rm uwsgi sh -c 'chgrp -R www-data .'
```

### Initialize Django tables

After inizialization, a new django user with administrative privilges is needed. This is
not the default postgres user, but a user valid only in django environment. Moreover
the django tables need to be defined:

```
$ docker-compose run --rm uwsgi python manage.py check
$ docker-compose run --rm uwsgi python manage.py migrate
$ docker-compose run --rm uwsgi python manage.py makemigrations
$ docker-compose run --rm uwsgi python manage.py migrate
$ docker-compose run --rm uwsgi python manage.py createsuperuser
```

The last commands will prompt for a user creation. This will be a new django
admin user, not the database users described in `env` files. Track user credentials
since those will be not stored in `.env` file of `shiny-server` directory.

### check that everythong works as expected

Test  your fresh InjectTool installation with:

```
$ docker-compose run --rm uwsgi pytest
```

Start composed image
--------------------

Pages are served by an nginx docker container controlled by Docker Compose
(see the docker-compose.yml file content). In order to start the service:

```
$ docker-compose up -d
```

The shiny-server interface is available for a local access through Internet browser
at the URL: `http://localhost:22080/`.
