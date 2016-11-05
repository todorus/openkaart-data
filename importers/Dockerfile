# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y git python python-dev python-distribute python-pip libpq-dev

# Get the app and dependencies
COPY code /importers
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# import data to process
COPY data /data

#start the scraper
WORKDIR importers
CMD python run_importers.py
