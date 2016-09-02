#!/bin/sh

wget http://download.geofabrik.de/south-america/peru-latest.osm.pbf
PROJECT_NAME=$(basename `pwd` | tr -cd '[[:alnum:]]')
POSTGIS_IP=$(docker inspect --format "{{ .NetworkSettings.Networks.${PROJECT_NAME}_default.IPAddress }}" "${PROJECT_NAME}_postgis_1") 
echo 'NOTE: get password from docker-compose.yml'
echo $POSTGIS_IP
osm2pgsql -s -U topicos -d topicos -H $POSTGIS_IP -W peru-latest.osm.pbf
