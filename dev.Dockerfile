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

# Configure database
USER postgres
COPY create_database.sql create_database.sql
RUN service postgresql start && \
    psql -f create_database.sql && \
    service postgresql stop

# Get the apps dependencies
USER root
COPY scrapers scrapers
RUN pip install -r scrapers/requirements.txt

# create the database tables
RUN service postgresql start && \
    psql -U postgres -d openkaart_development -c "CREATE EXTENSION postgis;" && \
    python scrapers/create_database_tables.py  && \
    service postgresql stop

# Create data directories
RUN mkdir -p /Volumes/openkaart_data/

# make sure postgres is running and start the scraper
CMD service postgresql start && \
    bin/bash
