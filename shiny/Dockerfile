#
# VERSION 0.5
# DOCKER-VERSION  17.05.0-ce
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A shiny container based on rocker-shiny
# TO_BUILD:       docker build --rm -t ibba/shiny .
# TO_RUN:         docker run -d -P ibba/shiny
# TO_TAG:         docker tag ibba/shiny:latest ibba/shiny:0.5
#

# Get the last rocker/shiny image
FROM rocker/shiny:3.6.1

# The mainteiner of this image
LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it"

# install package dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libxml2-dev \
    libpq-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/

# Install polished packages
COPY polished.r /root/
RUN Rscript --slave --vanilla /root/polished.r

# Install R packages. Packages are listed in packages.txt
COPY install.r packages.txt /root/
RUN Rscript --slave --vanilla /root/install.r

# Make sure the directory for individual app logs exists
RUN mkdir -p /var/log/shiny-server
RUN chown shiny.shiny /var/log/shiny-server

# change user
USER shiny

# override the defaul CMD (put stdout and stderr in docker stdout and stderr)
CMD ["shiny-server"]
