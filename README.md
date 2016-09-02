## Installation

```sh
git clone https://github.com/openstreetmap/mapnik-stylesheets
cd mapnik-stylesheets
./get-coastlines.sh
cd ..
docker-compose pull
```

### For development

```sh
docker-compose up -d
```

### For production
```sh
docker-compose -f docker-compose.prod.yml up -d
```
