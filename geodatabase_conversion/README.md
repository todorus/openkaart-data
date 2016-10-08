File GeoDatabase converter
=====================
*Docker container to convert ESRI file database containing some layers to GeoJSON
for us to use.*

Install docker
-------------
https://docs.docker.com/engine/installation/

Initializing the container
-----------------------
Either get it from the docker repository
```
docker pull todorus/openkaart-postal-areas
```
Or build it yourself
```
docker build . -t openkaart-postal-areas
```
The docker container is going to need access to your database file. So start the
container with a reference to the directory on your machine hosting the container.
The generated GeoJSON will be stored in this directory as well.
```
docker run -it -v {YOUR_DATA_DIR}:/home todorus/openkaart-postal-areas:latest /bin/bash
```
You are now in the docker container and should be able to see your data dir when
you navigate to /home.
```
cd /home
ls
```

Converting to GeoJSON
---------------------
GDAL and Proj-4 are installed on the container so we can use the ogr2ogr command to convert
any supported data format to the data format we want. In our case this is GeoJSON,
so this will be used in the following examples.

```
ogr2ogr -t_srs EPSG:4326 -f "GeoJSON" {OUTPUT_FILE} {YOUR_SOURCE_FILE}
```
* *t_srs: target projection. EPSG:4326 is used by Google maps and Leaflet*
* *-f: target format and output file*

You can run into the problem that you need to specify the projection the source
file uses as well. You can add this with the option -s_srs. For example, the
Dutch mapping authority uses EPSG:28992 so we can specify this to make sure
ogr2ogr uses this projection.
```
ogr2ogr -s_srs EPSG:28992 -t_srs EPSG:4326 -f "GeoJSON" {OUTPUT_FILE} {YOUR_SOURCE_FILE}
```

Converting a specific layer
---------------------------
We can use ogrinfo to find out more about the source data file
```
ogrinfo {YOUR_SOURCE_FILE}
```
Then we can use the ogr2ogr command to convert only data from that specific
layer.
```
ogr2ogr -t_srs EPSG:4326 -f "GeoJSON" {OUTPUT_FILE} {YOUR_SOURCE_FILE} {LAYER_NAME}
```
