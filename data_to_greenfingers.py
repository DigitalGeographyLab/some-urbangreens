
"""
Join grids which contain count data from social media and PPGIS with mobile phone data grid

"""
import geopandas as gpd
import pandas as pd
import os

fp = r"D:/ViherSOME/Data/YKR_grid/YKR_250m_Helsinki_centroidin_VISTRA_Vihersormi_fixedgeom.shp"
greengrid = gpd.read_file(fp)

datadir = r"P:\h510\some\data\finland\vihersome_temp"
grid = gpd.read_file(os.path.join(datadir, r'urbangreens_grid.gpkg'), layer="grid")

# Drop columns to avoid duplicate columns in merge
grid.drop(columns= ["x", 'GRIDCODE', 'x', 'y', 'xyind', 'Shape_Leng', 'Shape_Area', "geometry"], inplace = True)
greengrid.drop(columns= ['join_fid', 'join_id', 'join_kohde', 'distance'], inplace = True)

greengrid = greengrid.merge( grid, how = "inner",on = "ID", right_index = False)


# save output to file

xx.to_file(os.path.join(datadir, "urbangreens_grid.gpkg"), layer="grid", driver="GPKG")