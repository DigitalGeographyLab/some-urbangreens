
"""
Join user-generated data sets (PPGIS and Social media) to statistical grid 
including count of users (and count of userdays for social media data).

# INPUT DATA:
    - GRID (250 m x 250 m)
    - POINTS
    
# OUTPUT:
    - Grid geometry and user statistics from different point layers stored as one layer in a geopackage
"""

import geopandas as gpd
import pandas as pd
import os


def create_user_days(points):
    """ Generates a combination of day + month + user as a series"""

    # CONCATENATE USER + DAY + MONTH
    points["time_local"] = pd.to_datetime(points["time_local"])
    points_with_userday = points.apply(lambda x: str(x["time_local"].year) + str(x["time_local"].day) + str(x["time_local"].month) + "_" + str(x["userid"]), axis=1)

    return points_with_userday


def join_points_to_grid(points, grid):
    "joins attributes from points to intersecting polygons (left join)"

    # re-project points to grid crs
    points = points.to_crs(grid.crs)
    print("projected points into:", str(points.crs))
    grid_join = gpd.tools.sjoin(grid, points,  how="left", op="intersects")

    return grid_join


def count_per_grid(grid_join, grid_orig, value_column = "userday", group_column = "GRIDCODE"):
    """ groups the join (between grid and points), and counts unique values of selected column for each grid cell.
    Adds a count column to the original dataframe."""

    counts = pd.DataFrame(grid_join.groupby(group_column)[value_column].nunique())
    grid_ok = pd.merge(grid_orig, counts, left_on= group_column, right_index=True)

    return grid_ok

if __name__ == "__main__":

    # Input layers:

    # YKR grid polygons:
    grid_fp = r"D:\ViherSOME\Data\YKR_grid\YKR_250m_Helsinki.shp"
    grid = gpd.read_file(grid_fp)
    polygon_id = "ID"

    datadir = r"P:\h510\some\data\finland\vihersome_temp"

    # List layers for analysis (these exist in the geodatabase
    # Dictionary contains info of layername: type
    layers = {"PPGIS2050_greens" : "PPGIS",
              "PPGISpark_greens" : "PPGIS",
              "insta_helsinki_2015_greens": "socialmedia",
              "flick_helsinki_2015_greens": "socialmedia",
              "twitt_helsinki_2017_greens": "socialmedia"}

    # Dictionary contains info of layername: unique user id column
    usercolumns = {"PPGIS2050_greens" :'user_id',
              "PPGISpark_greens":'respondent',
              "insta_helsinki_2015_greens":'userid',
              "flick_helsinki_2015_greens":'userid',
              "twitt_helsinki_2017_greens":'userid'}

    for layer, type in layers.items():

        # Read in layer from geopackage
        df = gpd.read_file(os.path.join(datadir, r'urbangreens.gpkg'), layer=layer)
        df.crs = {'init': 'epsg:4326'}

        if type == "socialmedia":
            # continue only with user id column and timestamp
            df = df[[usercolumns.get(layer), "time_local", "geometry"]]

            # apply:
            df["userday"] = create_user_days(df)

        if type == "PPGIS":
            # continue only with user id column and timestamp
            df = df[[usercolumns.get(layer), "geometry"]]

        # Join point info to intersecting grid; left join which returns all combinations
        join = join_points_to_grid(df, grid)
        grid = count_per_grid(join, grid, value_column = usercolumns.get(layer), group_column = polygon_id)

        grid.rename(columns = {usercolumns.get(layer): layer[:9] + "_users"}, inplace=True)

        if type == "socialmedia":
            #Count also userdays per grid
            grid = count_per_grid(join, grid, value_column="userday", group_column=polygon_id)
            grid.rename(columns={"userday": layer[:9] + "_userdays"}, inplace=True)

    #save output to file
    grid.to_file(os.path.join(datadir, "urbangreens_grid.gpkg"), layer = "grid", driver="GPKG")
