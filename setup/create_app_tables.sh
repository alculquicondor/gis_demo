#!/bin/sh

PROJECT_NAME=$(basename `pwd` | tr -cd '[[:alnum:]]')
POSTGIS_IP=$(docker inspect --format "{{ .NetworkSettings.Networks.${PROJECT_NAME}_default.IPAddress }}" "${PROJECT_NAME}_postgis_1")

echo 'NOTE: get password from docker-compose.yml'
psql -h ${POSTGIS_IP} -W -U topicos < setup/areas_and_places.sql
