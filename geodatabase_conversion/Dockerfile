# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y git python python-dev python-distribute python-pip libpq-dev

# Install 4.8 version of C++ compiler, as newer versions seem to be incompatible
# with GDAL (see http://stackoverflow.com/questions/34907331/filegdb-make-fails-for-sample-ubuntu-15)
# RUN apt-get install -y g++-4.8

#
# Install GDAL/OGR with FileGDB
#
RUN apt-get install -y build-essential wget
# later versions may be found here: http://appsforms.esri.com/products/download
RUN wget http://appsforms.esri.com/storage/apps/downloads/software/filegdb_api_1_4-64.tar.gz
RUN tar xfv filegdb_api_1_4-64.tar.gz && \
    mv /FileGDB_API-64/ /usr/local/FileGDB_API/
# configure links
RUN echo "/usr/local/FileGDB_API/lib" >> /etc/ld.so.conf && \
    ldconfig
# get gdal
RUN wget http://download.osgeo.org/gdal/2.1.1/gdal-2.1.1.tar.gz && \
    tar xfv gdal-2.1.1.tar.gz
WORKDIR /gdal-2.1.1
RUN CXXFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" ./configure --with-python --with-fgdb=/usr/local/FileGDB_API
RUN make clean && \
    make && \
    make install && \
    ldconfig

#
# Install PROJ.4
#
RUN mkdir /proj4
WORKDIR /proj4
RUN wget http://download.osgeo.org/proj/proj-4.9.1.tar.gz
RUN wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz
RUN tar xzf proj-4.9.1.tar.gz
WORKDIR /proj4/proj-4.9.1
RUN cd nad && \
    tar xzf /proj4/proj-datumgrid-1.5.tar.gz
RUN ./configure && \
    make && \
    make install && \
    ldconfig

#
# Run it
#
WORKDIR /home
# data from:
# https://www.arcgis.com/home/signin.html?returnUrl=http%3A%2F%2Fwww.arcgis.com%2Fhome%2Fgroup.html%3Fowner%3DEsri_NL_Datasets%26title%3DDatasets%2520-%2520Esri%2520Nederland
CMD wget https://drive.google.com/drive/folders/0B41FwEmSlm8JTHdSemJuQVdkX1k?usp=sharing -O Postcodevlakken.gdb && \
    ogr2ogr -progress -t_srs EPSG:4326 -s_srs EPSG:28992 -f "GeoJSON" postcodes.geo.json Postcodevlakken.gdb PC4
