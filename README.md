# shp2geojson
## Parsing cadastral spatial data to GEOJSON in MacOS

#### Requirements
* Python 3.6
* PyQt 5
* [GDAL : ogr2ogr](https://github.com/wavded/ogr2ogr)
* QGIS (I used the path from [osgeo/osgeo4mac](https://github.com/OSGeo/homebrew-osgeo4mac#how-do-i-install-these-formulae))
```
brew tap osgeo/osgeo4mac
brew install osgeo/osgeo4mac/qgis
```

There are two ways to test out this code.

**Standalone script in terminal**

Check whether all requirements are met, check if all the paths are correct, then run the bash script `./script.sh`.

All geojson files are now in `geojson` folder.

**Through Python console in QGIS (GUI)**

* Install [QGIS](https://qgis.org)
* Plugins > Python Console
This can only process each layer at once, please ensure the path to each shp layer
is correct.

```python
layer = QgsVectorLayer("path/to/file/M4442A_palstaalue.shp", "M4442A_shp", "ogr")

if not layer.isValid():
  print "Layer failed to load!"

layer = iface.activeLayer()
provider = layer.dataProvider()

areas = [ feat.geometry().area()
       for feat in layer.getFeatures() ]

field = QgsField("area", QVariant.Double)
provider.addAttributes([field])
layer.updateFields()

idx = layer.fields().indexFromName('area')

for area in areas:
    new_values = {idx : float(area)/10000}
    provider.changeAttributeValues({areas.index(area):new_values})

res = layer.dataProvider().deleteAttributes([1])
layer.updateFields()
```
Export file through QGIS by right click at the layer > Save Feature as > Format: GEOJSON

or
```
ogr2ogr -f GeoJSON -t_srs crs:84 M4442A.geojson /path/to/file/M4442A_palstaalue.shp
```
