#!/usr/bin/env python
from cStringIO import StringIO
import json

from flask import Flask, send_file, request, jsonify
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


@app.route('/base_layer/<int:z>/<int:x>/<int:y>.png', methods=['GET'])
def base_layer(z, x, y):
    config = parseConfigfile('tiles.conf')
    content_type, tile = getTile(config.layers['peru'], Coordinate(y, x, z),
                                 'png')
    return send_file(StringIO(tile), mimetype=content_type)


@app.route('/areas', methods=['GET', 'POST'])
def areas_list():
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == 'GET':
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

    else:
        result = {}

    cursor.close()
    connection.close()
    return jsonify(result)


if __name__ == '__main__':
    app.run()
