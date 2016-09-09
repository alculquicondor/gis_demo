#!/usr/bin/env python
from cStringIO import StringIO
import json

from flask import Flask, send_file, request, jsonify, abort
from ModestMaps.Core import Coordinate
import psycopg2
import psycopg2.extras
from TileStache import parseConfigfile, getTile

import settings

app = Flask(__name__)


def get_connection():
    db_params = dict(**settings.DB_PARAMS)
    db_params['cursor_factory'] = psycopg2.extras.DictCursor
    return psycopg2.connect(**db_params)


@app.errorhandler(400)
def json400(error):
    response = jsonify({'message': error.description})
    response.status_code = 400
    return response


@app.route('/base_layer/<int:z>/<int:x>/<int:y>.png')
def base_layer(z, x, y):
    config = parseConfigfile('tiles.conf')
    content_type, tile = getTile(config.layers['peru'], Coordinate(y, x, z),
                                 'png')
    return send_file(StringIO(tile), mimetype=content_type)


@app.route('/areas')
def areas_list():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT id, name, ST_ASGEOJSON(geometry) as geometry '
                   'FROM gisdemo_area')
    features = []
    for row in cursor.fetchall():
        features.append({
            'type': 'Feature',
            'geometry': json.loads(row['geometry']),
            'properties': {
                'id': row['id'],
                'name': row['name']
            }
        })
    result = {
        'type': 'FeatureCollection',
        'features': features
    }

    cursor.close()
    connection.close()
    return jsonify(result)


@app.route('/areas/create', methods=['POST'])
def area_create():
    data = request.json
    if not isinstance(data, dict):
        abort(400, 'not a valid JSON')
    if (data.get('type') != 'Feature' or
            not isinstance(data.get('geometry'), dict)):
        abort(400, 'not a Feature')
    properties = data.get('properties')
    if not isinstance(properties, dict):
        abort(400, 'properties missing')
    name = properties.get('name')
    if not isinstance(name, basestring) or not name:
        abort(400, 'invalid name property')
    geometry = data.get('geometry')
    if not isinstance(geometry, dict):
        abort(400, 'invalid geometry')
    geometry['crs'] = {
        'type': 'name',
        'properties': {'name': 'EPSG:4326'}
    }

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO gisdemo_area (name, geometry) '
                       'VALUES (%s, ST_GEOMFROMGEOJSON(%s)) RETURNING id',
                       (name, json.dumps(geometry)))
        row = cursor.fetchone()
        del geometry['crs']
        feature = {
            'type': 'Feature',
            'geometry': geometry,
            'properties': {
                'id': row['id'],
                'name': name
            }
        }
    except psycopg2.DatabaseError as exc:
        abort(400, str(exc))
    else:
        connection.commit()
        return jsonify(feature)
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run()
