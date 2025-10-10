#
# VERSION 0.7
# DOCKER-VERSION  28.5.0
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A shiny container based on rocker-shiny
# TO_BUILD:       docker build --rm -t bunop/shiny-server_shiny .
#

# Get the last rocker/shiny image
FROM rocker/shiny:4.5.1

# The maintainer of this image
LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it>"
LABEL R.version="4.5.1"
LABEL description="A shiny container based on rocker-shiny"

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# install package dependencies
RUN apt-get update && apt-get install -y \
    git \
    libssl-dev \
    libxml2-dev \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libwebp-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/

# Install R packages. Packages are listed in packages.txt
COPY install.r packages.txt /root/
RUN Rscript --slave --vanilla /root/install.r

# Make sure the directory for individual app logs exists
RUN mkdir -p /var/log/shiny-server
RUN chown shiny.shiny /var/log/shiny-server

# set a global renv cache path
ENV RENV_PATHS_ROOT=/srv/renv-cache
ENV RENV_PATHS_LIBRARY_ROOT=/srv/renv-cache/library

RUN mkdir -p /srv/renv-cache && \
    chown -R shiny:shiny /srv/renv-cache

# set the renv cache path in Renviron
RUN echo "RENV_PATHS_ROOT=/srv/renv-cache" >> /usr/local/lib/R/etc/Renviron && \
    echo "RENV_PATHS_LIBRARY_ROOT=/srv/renv-cache/library" >> /usr/local/lib/R/etc/Renviron

# change user
USER shiny

# set log directory as volume log
VOLUME /var/log/shiny-server

# other volumes
VOLUME /srv/shiny-server
VOLUME /srv/renv-cache

# change to the shiny app directory
WORKDIR /srv/shiny-server/

# override the default CMD (put stdout and stderr in docker stdout and stderr)
CMD ["shiny-server"]
