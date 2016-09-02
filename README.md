## Installation

### Pre-requisites

You need to install:

- [Docker](https://docs.docker.com/engine/installation/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Osm2pgsql](http://wiki.openstreetmap.org/wiki/Osm2pgsql)

```sh
# Getting OSM's Mapnik files
git clone https://github.com/openstreetmap/mapnik-stylesheets
cd mapnik-stylesheets
./get-coastlines.sh

# Creating containers
cd ..
docker-compose pull
docker-compose up -d
# or `docker-compose -f docker-compose.prod.yml up -d` if you don't intent to develo'

# Filling up OSM data
./fill_osm_data.sh
```
