#!/usr/bin/env python
from cStringIO import StringIO

from flask import Flask, send_file
from ModestMaps.Core import Coordinate
from TileStache import parseConfigfile, getTile

app = Flask(__name__)


@app.route('/base_layer/<int:z>/<int:x>/<int:y>.png')
def base_layer(z, x, y):
    config = parseConfigfile('tiles.conf')
    content_type, tile = getTile(config.layers['peru'], Coordinate(y, x, z), 'png')
    return send_file(StringIO(tile), mimetype=content_type)


if __name__ == '__main__':
    app.run()
