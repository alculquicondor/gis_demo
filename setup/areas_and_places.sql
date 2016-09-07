BEGIN;

DROP TABLE IF EXISTS gisdemo_area;
DROP TABLE IF EXISTS gisdemo_place;

CREATE TABLE gisdemo_area (
  id SERIAL, nombre TEXT NOT NULL);
SELECT AddGeometryColumn('gisdemo_area', 'geometry', 4326, 'POLYGON', 2);

CREATE TABLE gisdemo_place (
  id SERIAL, nombre TEXT NOT NULL);
SELECT AddGeometryColumn('gisdemo_place', 'geometry', 4326, 'POINT', 2);

COMMIT;