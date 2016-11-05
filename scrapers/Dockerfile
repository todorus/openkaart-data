# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y git python python-dev python-distribute python-pip libpq-dev

# Install Postgres and PostGis
RUN apt-get install -y postgresql-9.5 postgresql-contrib-9.5 postgis-2.2
RUN sed -i 's/peer/trust/g' /etc/postgresql/9.5/main/pg_hba.conf

# Get the app and dependencies
RUN git clone -b develop https://github.com/todorus/openkaart-data.git
RUN pip install -r openkaart-data/scrapers/requirements.txt

# Create data directories
RUN mkdir -p /Volumes/openkaart_data/

# make sure postgres is running and start the scraper
VOLUME /Volumes/openkaart_data/
WORKDIR /openkaart-data/scrapers
CMD git pull && \
    python run_scrapers.py
