
"""
Subset social media posts for green areas
Also prints statistics about proportion of city-wide data sets in green space (Table 3 in manuscript).

The starting point for this script is the output of "get_postgis_data.py", which fetches data
from the DigiGeoLab database.

# Input:
    -Public green areas: "YLRE_Viheralue_alue" from https://kartta.hel.fi/ws/geoserver/avoindata/wfs
    -Geopackage containing Helsinki-wide point data for
        Instagram 2015
        Flickr 2015
        Twitter 2017
#Output:
    Stores new layers in geopackage containing points from green areas. epsg:4326
        Instagram
        Flickr
        Twitter

Author: Vuokko H. (4.7.2019)

"""
import geopandas as gpd
import os

def spatial_subset(points, polygon):
    "Returns points intersecting the polygon. Output crs: epsg 4326."

    if points.crs != polygon.crs:
        points = points.to_crs(polygon.crs)
        point_subset = gpd.tools.sjoin(points, polygon, how='inner', op="intersects")
        point_subset = point_subset.to_crs(crs = {'init': 'epsg:4326'})

    return point_subset

# Green area
url = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs?request=GetFeature&service=WFS&version=1.1.0&typeName=avoindata:YLRE_Viheralue_alue&outputFormat=JSON"
greenarea = gpd.read_file(url)
greenarea = greenarea[greenarea['geometry'].notnull()] # the layer has one empty geometry
greenarea.crs = {'init' :'epsg:3879'}

# Social media points
datadir = r"P:\h510\some\data\finland\vihersome_temp"

layers = ["insta_helsinki_2015","flick_helsinki_2015","twitt_helsinki_2017"]

for layer in layers:
    # Read in layer from geopackage
    df = gpd.read_file(os.path.join(datadir, r'urbangreens.gpkg'), layer=layer)
    df.crs = {'init': 'epsg:4326'}

    if layer == "twitt_helsinki_2017":
        df.drop_duplicates(subset = "id", inplace = True)
    else:
        df.drop_duplicates(subset="photoid", inplace=True)

    # PRINT INFO
    print(layer)
    print("\t", len(df), "posts in Helsinki")
    print("\t", df.userid.nunique(), "users in Helsinki")

    # Posts in Helsinki green areas
    greenareapoints = spatial_subset(df, greenarea)

    print("\t", len(greenareapoints), "in greens", "{0:.0%}".format(len(greenareapoints) / len(df)))
    print("\t", greenareapoints.userid.nunique(), "users in greens", "{0:.0%}".format(greenareapoints.userid.nunique() / df.userid.nunique()))

    # Save output layer to geopackage
    print("saving green area posts from ", layer)
    greenareapoints.to_file(os.path.join(datadir, "urbangreens.gpkg"), layer = layer + "_greens", driver="GPKG")


