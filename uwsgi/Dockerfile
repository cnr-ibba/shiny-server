
#
# VERSION 0.8
# DOCKER-VERSION  17.05.0-ce
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A django container working on LTS django 2.2 on python 3
# TO_BUILD:       docker build --rm -t bunop/shiny-server_uwsgi .
#

# The official django image is deprecated in favor of the standard python image
FROM python:3.8

# The mainteiner of this image
LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it"

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    default-mysql-client \
    sqlite3 && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

# Create directory for a django project
RUN mkdir /var/uwsgi/

# Set corrent working directory
WORKDIR /var/uwsgi/

# Set uwsgi directory as VOLUME
VOLUME /var/uwsgi/

# Expose the default port for django
EXPOSE 8000

# This environment variable force stdin, stdout and stderr to be totally unbuffered
ENV PYTHONUNBUFFERED 1

# Install pypi modules (uwsgi)
COPY requirements.txt /root/
RUN pip install --no-cache-dir -r /root/requirements.txt

# utility script to ensure that postgres server is up
COPY wait-for-mysql.sh /root/

# Execute a default command
CMD ["/bin/bash"]
