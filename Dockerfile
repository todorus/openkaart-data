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
RUN git clone -b feature/scraper https://github.com/todorus/openkaart-api.git
RUN pip install -r openkaart-api/scrapers/requirements.txt

# Configure database
USER postgres
RUN service postgresql start && \
    psql -f openkaart-api/create_database.sql && \
    service postgresql stop

# create the database tables
USER root
RUN service postgresql start && \
    psql -U postgres -d openkaart_development -c "CREATE EXTENSION postgis;" && \
    python openkaart-api/scrapers/create_database_tables.py  && \
    service postgresql stop

# Create data directories
RUN mkdir -p /Volumes/openkaart_data/
COPY scrapers/postgresql.conf /etc/postgresql/9.5/main/postgresql.conf

# make sure postgres is running and start the scraper
VOLUME /Volumes/openkaart_data/
WORKDIR /openkaart-api/scrapers
CMD if [ ! -d "/Volumes/openkaart_data/postgresql" ]; then rsync -av /var/lib/postgresql/9.5/main/ /Volumes/openkaart_data/postgresql; fi && \
    service postgresql start && \
    git pull && \
    python run_scrapers.py
