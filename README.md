
Shiny-django authentication
===========================

[![Django Tests](https://github.com/cnr-ibba/shiny-server/actions/workflows/django-tests.yml/badge.svg)](https://github.com/cnr-ibba/shiny-server/actions/workflows/django-tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/cnr-ibba/shiny-server/badge.svg)](https://coveralls.io/github/cnr-ibba/shiny-server)
![GitHub](https://img.shields.io/github/license/cnr-ibba/shiny-server)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/cnr-ibba/shiny-server)

This is an attempt of managing shiny authentication with django starting from
[Django application as an authentication / authorization server for Shiny](http://pawamoy.github.io/2018/03/15/django-auth-server-for-shiny/)
guide and modifying stuff accordingly. The django template derive from
[this repository](https://github.com/cnr-ibba/dockerfiles/tree/master/compose/django)
while the shiny specific configuration comes from [here](https://github.com/cnr-ibba/dockerfiles/tree/master/compose/shiny).
The aim of this project is to provide both free and restricted access to shiny
applications relying on django authentication system and nginx. Applications could
be accessed using the django frontend as a container of an iframe application or
directly by specifying the path of the application. A specific NGINX configuration
will be responsible to provide access to shiny applications relying on django
authentication system.

If you need more information please see our
[Wiki on GitHub](https://github.com/cnr-ibba/shiny-server/wiki)

Install dependencies
--------------------

All this stuff works inside a docker compose image and need [docker](https://www.docker.com/)
and [docker compose](https://docs.docker.com/compose/) to work. Please refer to
the official documentation on how to install [docker](https://docs.docker.com/install/)
and [docker compose](https://docs.docker.com/compose/install/)

Install shiny-server
--------------------

The `shiny-server` project is composed by four different docker containers:
- `db`: a MySQL database which stores information about users credentials
- `shiny`: a `rocker/shiny` based images with few dependencies installed to render
  shiny applications
- `uwsgi`: a Django base image which implements views and authentication system
- `nginx`: used as a proxy to connect `shiny` and `uwsgi` backends. A special
  configuration location lets to provide shiny contents to authenticated users

Clone this project and enter in project directory:

```bash
git clone https://github.com/cnr-ibba/shiny-server.git
cd shiny-server
```

This location will be referred as **working directory**, since all commands need
to be launched inside this directory. This directory will also contains all the
shiny application data, database and configuration files.

### Setting up the environment file

`docker compose` can read environment variables from a `.env` placed in the working
directory in which we can define all variables useful for our containers, like database
credentials. Edit a new `.env` file in working directory and set values for such
environment variables accordingly:

```conf
MYSQL_ROOT_PASSWORD=<root_password>
SHINY_DATABASE=<shiny_db>
SHINY_USER=<shiny_user>
SHINY_PASSWORD=<shiny_password>
SECRET_KEY=<your SECRET_KEY>
DEBUG=False
ADMINS=<admin name1>:<admin email>
DEFAULT_FROM_EMAIL=<your email from>
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=<your stmp server>
EMAIL_HOST_PASSWORD=<your smtp password>
EMAIL_HOST_USER=<your smtp password>
EMAIL_PORT=<your email port address>
EMAIL_USE_TLS=<set 'True' to use TLS, false otherwise
```

### Build the docker compose suite

In order to build the images according to the `docker-compose.yml` specifications,
Docker needs download and install all required dependencies; it will need several
minutes to complete. Launch this command from the working directory:

```bash
docker compose build
```

### Fixing django permissions

You will also to check file permissions in `django-data` folder, expecially for `media`
folder:

```bash
docker compose run --rm -u $(id -u):www-data uwsgi sh -c 'chmod -R g+rw media && chmod g+rwx media/thumbnails/'
docker compose run --rm -u $(id -u):www-data uwsgi sh -c 'chgrp -R www-data .'
```

### Initialize Django tables

After inizialization, a new django user with administrative privilges is needed. This is
not the default mysql user, but a user valid only in django environment. Moreover
the django tables need to be defined:

```bash
docker compose run --rm -u $(id -u):www-data uwsgi python manage.py check
docker compose run --rm -u $(id -u):www-data uwsgi python manage.py migrate
docker compose run --rm -u $(id -u):www-data uwsgi python manage.py makemigrations
docker compose run --rm -u $(id -u):www-data uwsgi python manage.py migrate
docker compose run --rm -u $(id -u):www-data uwsgi python manage.py createsuperuser
```

The last commands will prompt for a user creation. This will be a new django
admin user, not the database users described in `env` files. Track user credentials
since those will be not stored in `.env` file in `shiny-server` directory.

### Check everything works as expected

Test  your fresh InjectTool installation with:

```bash
docker compose run --rm -u $(id -u):www-data uwsgi pytest
```

Start composed image
--------------------

Pages are served by an nginx docker container controlled by Docker Compose
(see the `docker-compose.yml` file content), which is linked to the shiny
server and django instance. In order to start the application:

```bash
docker compose up -d
```

The shiny-server interface is available for a local access through Internet browser
at the URL: `http://localhost:22080/`.
