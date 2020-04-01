#
# VERSION 0.5
# DOCKER-VERSION  17.05.0-ce
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A shiny container based on rocker-shiny
# TO_BUILD:       docker build --rm -t bunop/shiny-server_shiny .
#

# Get the last rocker/shiny image
FROM rocker/shiny:3.6.1

# The mainteiner of this image
LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it"

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# install package dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libxml2-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/

# Install R packages. Packages are listed in packages.txt
COPY install.r packages.txt /root/
RUN Rscript --slave --vanilla /root/install.r

# Make sure the directory for individual app logs exists
RUN mkdir -p /var/log/shiny-server
RUN chown shiny.shiny /var/log/shiny-server

# change user
USER shiny

# set log directory as volume log
VOLUME /var/log/shiny-server

# override the defaul CMD (put stdout and stderr in docker stdout and stderr)
CMD ["shiny-server"]
