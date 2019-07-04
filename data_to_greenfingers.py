
"""
Join data to green area grids.

# Input
    - grid containing cells with their centroids inside green fingers (VISTRA). Layer created in QGIS
    - grid containing count data from social media and PPGIS
    - grid containing relative hourly population density based on mobile phone data (Bergroth 2019)

# Output
    - grid with information from user-generated data sources covering the green fingers in Helsinki
    - stored as a layer in geopackage

Author: Vuokko H. 4.7.2019

"""
import geopandas as gpd
import pandas as pd
import os

# Grid cells with centroids in green areas (generated using QGIS :) )
fp = r"D:/ViherSOME/Data/YKR_grid/YKR_250m_Helsinki_centroidin_VISTRA_Vihersormi_fixedgeom.shp"
greengrid = gpd.read_file(fp)

# Full grid with social media data and PPGIS counts
datadir = r"P:\h510\some\data\finland\vihersome_temp"
grid = gpd.read_file(os.path.join(datadir, r'urbangreens_grid.gpkg'), layer="grid")

# Mobile phone data for the whole Helsinki Region
fp = "D:\ViherSOME\Data\Mobile_phone\dynamic_population_24H.csv"
mobile = pd.read_csv(fp)

# Drop columns to avoid duplicate columns in merge
grid.drop(columns= ["x", 'GRIDCODE', 'x', 'y', 'xyind', 'Shape_Leng', 'Shape_Area', "geometry"], inplace = True)
greengrid.drop(columns= ['join_fid', 'join_id', 'join_kohde', 'distance'], inplace = True)
mobile.drop(columns= ["Unnamed: 0", "geometry"], inplace = True)

#merge social media, PPGIS to greengrid
greengrid = greengrid.merge( grid, how = "inner",on = "ID", right_index = False)

# merge mobile phone data to grid:
greengrid = greengrid.merge(mobile, left_on = "ID", right_on = "YKR_ID")

# save output to file
print("Saving output to geopackage")
greengrid.to_file(os.path.join(datadir, "urbangreens_grid.gpkg"), layer="greengrid", driver="GPKG")