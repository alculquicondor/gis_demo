FROM python:2
MAINTAINER Aldo Culquicondor "alculquicondor@gmail.com"

RUN apt-get update && apt-get install -y python-mapnik \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /srv/gis
COPY app/tiles.conf app/peru.xml ./
COPY app/gis.py .

CMD gunicorn -b 0.0.0.0:8000 -w 2 gis:app
