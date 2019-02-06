# Uyen Truong, 2018
# Process Shapefiles and export them to GEOJSON

#!/usr/local/Cellar/qgis/3.4.4_1/libexec/vendor/bin/python

import os, sys
import re
import PyQt5
sys.path.append('/usr/local/Cellar/qgis/3.4.4_1/QGIS.app/Contents/Resources/python')

from qgis.core import *
from PyQt5.QtCore import QVariant

app = QgsApplication([],True)
QgsApplication.setPrefixPath(r"/usr/local/Cellar/qgis/3.4.4_1/QGIS.app/Contents/MacOS", True)
QgsApplication.initQgis()

# Process to calculate area and delete extra columns
def processSHP(layer):
    # Calculate area in hect from polygon
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

    # Delete unnecessary attribute columns
    res = layer.dataProvider().deleteAttributes([1])
    layer.updateFields()

# List files in directory
fileList = os.listdir("./")
fileSHP = []

# Add needed shapefiles name to fileSHP list
for i in range(len(fileList)):
    if re.match(r".*_palstaalue.shp", fileList[i]):
        fileSHP.append("./" + fileList[i])

# Load each shapefile from list and process
for i in range(len(fileSHP)):
    layer = QgsVectorLayer(fileSHP[i], "SHP", "ogr")
    if not layer.isValid():
      print("Layer failed to load!")

    processSHP(layer)

app.exitQgis()
