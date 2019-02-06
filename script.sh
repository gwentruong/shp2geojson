#!/bin/bash

# Unzip all files in a directory
for var in *.zip; do unzip "$var"; done

# Set path to python program
python3 rakennus.py

# geojson conversion
function shp2geojson() {
  ogr2ogr -f GeoJSON -t_srs crs:84 "$1.geojson" "$1.shp"
}

#convert all shapefiles to GEOJSON
for var in ./*_palstaalue.shp; do shp2geojson ${var%\.*}; done
mkdir geojson
find ./ -name '*.geojson' -exec mv {} ./geojson \;
