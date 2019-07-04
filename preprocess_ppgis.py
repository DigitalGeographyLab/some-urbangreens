"""
This script

1. reads in the original PPGIS point markers
2. filters data based on bbox and attributes
3. selects data inside Helsinki
4. selects data inside public green space
5. stores layers in a geopackage

# Input layers:
    Contents of the datadir -folder are original point data downloaded from HRI:
    - PPGIS 2050: Helsinki 2050 survey results: https://hri.fi/data/en_GB/dataset/helsinki-2050-kyselyn-vastaukset
    - PPGIS park: Questionnaire about Helsinki's national city park: https://hri.fi/data/en_GB/dataset/helsingin-kansallinen-kaupunkipuisto-kyselyn-vastaukset

    PPGIS 2050 layer was converted to shp in QGIS prior to running this script.

# Output
    outputs new layers to a geopackage for each input layer:
    - all points in Helsinki
    - all points in Helsinki green areas

"""

import geopandas as gpd
import os

def spatial_subset(points, polygon):
    "creates a new geodatabase containing points intersecting the polygon. Output crs from polygon."

    if points.crs != polygon.crs:
        points = points.to_crs(polygon.crs)

    point_subset = gpd.tools.sjoin(points, polygon, how='inner', op="intersects")

    return point_subset

# DEFINE DATA DIRECTORIES HERE:
datadir = r"P:\h510\some\data\finland\PPGIS"
outfp = r"P:\h510\some\data\finland\vihersome_temp"

# municipality borders
url = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs?request=GetFeature&service=WFS&version=1.1.0&typeName=avoindata:Seutukartta_aluejako_kuntarajat&outputFormat=JSON"
area = gpd.read_file(url)
area = area[area["nimi"] == "Helsinki"]
area.crs = {'init' :'epsg:3879'}

# Green area
url = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs?request=GetFeature&service=WFS&version=1.1.0&typeName=avoindata:YLRE_Viheralue_alue&outputFormat=JSON"
greenarea = gpd.read_file(url)
greenarea = greenarea[greenarea['geometry'].notnull()] # the layer has one empty geometry
greenarea.crs =  {'init' :'epsg:3879'}

# PPGIS input layers
filenames = {"PPGISpark": r"kansallinen_kaupunkipuisto-kysely_updated\avoin_data_final_id\kansallinen_kaupunkipuisto_point.shp",
        "PPGIS2050":r"Helsinki_yleiskaava\Helsinki_2050_KML\hki_2050_pisteet_SHP.shp"}


for name, filepath in filenames.items():

    # Read in layer
    fullpath = os.path.join(datadir, filepath)
    file = gpd.read_file(fullpath)

    print("layer:", name, "--> number of recors: ")
    print("\t", len(file), "original")

    # use the cx method to filter extreme outliers before re-projection / spatial join
    # syntax: df.cx[xmin:xmax, ymin:ymax] / https://gis.stackexchange.com/questions/266730/filter-by-bounding-box-in-geopandas
    file = file.cx[23.0:26.0 , 59.0:61.0]

    print("\t", len(file), "after bbox")


    if name == "PPGIS2050":
        # Select rows for PPGIS 2050 survey
        helsinkipoints = spatial_subset(file, area)
        print("\t", len(helsinkipoints), "all data in in Helsinki")

        file = file[(file["valuename"] == 'taalla-on-tallaisenaan-ainutlaatuista-kaupunkiluontoa') |
                    (file["valuename"] == 'virkistyksellisesti-tarkea-mutta-saisi-olla-laadultaan-parempi')]
        print("\t", len(file), "all data after selecting attributes")


    # Posts in Helsinki
    helsinkipoints = spatial_subset(file, area)
    print("\t", len(helsinkipoints), "in Helsinki")

    # Posts in Helsinki green areas
    greenareapoints = spatial_subset(file, greenarea)
    print("\t", len(greenareapoints), "in greens","{0:.0%}".format(len(greenareapoints)/ len(helsinkipoints)))

    if name == "PPGIS2050":
        print("\t", "users in Helsinki:", helsinkipoints.user_id.nunique())
        print("\t", "users in greens:", greenareapoints.user_id.nunique())

    if name == "PPGISpark":
        print("\t", "users in Helsinki:", helsinkipoints.respondent.nunique())
        print("\t", "users in greens:", greenareapoints.respondent.nunique())

    helsinkipoints = helsinkipoints.to_crs(file.crs)
    greenareapoints = greenareapoints.to_crs(file.crs)

    # Save layers to geopackage:
    helsinkipoints.to_file(os.path.join(outfp, "urbangreens.gpkg"), layer = name + "_helsinki", driver = "GPKG")
    greenareapoints.to_file(os.path.join(outfp, "urbangreens.gpkg"), layer = name + "_greens", driver="GPKG")




