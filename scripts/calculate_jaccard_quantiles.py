""" Script for calculating the Jaccard index between the top 10 % spatial
hotspots of user-generated data sets in urban green areas.

Jaccard index: intersection divided by the union of two sets

Steps:
- Read in dataframe containing data counts in a grid
- Get top 10 % of each column (the hotspots)
- Calculate jaccard index (intersection over union) for each column pair
- save output matrix as csv

Input:
    YKR grid data with grid cells as rows
    and counts of user-generated content as columns (can be a shapefile, csv, whatever pandas reads)
Output:
    csv file with crosstabulated jaccard scores for data set pairs

Vuokko H. 21 May 2019

"""

import geopandas as gpd
import pandas as pd
import numpy as np
import os

#-----------------------------
# Read input data
#------------------------------

group_column = "YKR_ID" #"id" #

# Set the number of quantiles
quantiles = 5
layer = "greengrid"
version= "drop_duplicates_no_zero"

# input data
datadir = r"P:\h510\some\data\finland\vihersome_temp"
data = gpd.read_file(os.path.join(datadir, r'urbangreens_grid.gpkg'), layer=layer)

# result file
out_fp = r"jaccard_results_temp\jaccard_%s_q%s_%s.csv" % (layer, str(quantiles), version)

# metadata file
meta_fp = r"jaccard_results_temp\jaccard_%s_q%s_categories_%s.txt" % (layer, str(quantiles), version)
file1 = open(meta_fp,"w")
file1.close()

# geodata file name
quantilelayername = r"greengrid_q%s_%s_%s" % (str(quantiles), layer , version )

#check input data
print(data.head())
print(data.columns.values)

# Replace zero with nan to exclude from classification
#data.replace(to_replace=0, value=np.nan, inplace=True)

#select columns for comparison:
data_values = data[['PPGIS2050_users', 'PPGISpark_users', 'insta_hel_users',
        'flick_hel_users', 'twitt_hel_users', 'ZROP H16', 's_athlete__max']]

# Rename columns for output
data_values.rename(columns = {'PPGIS2050_users':'PPGIS2050',
                              'PPGISpark_users':'PPGISPark',
                              'insta_hel_users':'Instagram',
                              'flick_hel_users':'Flickr',
                              'twitt_hel_users':'Twitter',
                              'ZROP H16':'MobilePhone4PM',
                              's_athlete__max':'Strava'},
                   inplace = True)

#------------------------------
# Get top 10 % of each column
#------------------------------

# Discretize column values (axis = 0) into 10 equal-sized buckets; output as bins
#https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.qcut.html
#data_q = data_values.apply(lambda x: pd.qcut(x, q=10, duplicates="drop"), axis = 0)

# Discretize column values (axis = 0) into 10 equal-sized buckets; output as flexible-length labels
data_q = data_values.apply(lambda x: pd.qcut(x,
                                             q=quantiles,
                                             duplicates="drop",
                                             labels = range(0, len(pd.qcut(x,q=quantiles, duplicates="drop").value_counts()))), # as many labels as there are categories
                                             axis = 0)

# Store info about the quantile categories into a separate text file
for column in data_values.columns.values:
    file1 = open(meta_fp, "a")

    lines = ["#####################\n",
             "Categories for column " + column + "\n",
             str(pd.qcut(data_values[column],q=quantiles, duplicates="drop").values) + "\n",
             str(pd.qcut(data_values[column], q=quantiles, duplicates="drop").value_counts()),
            "\n\n",]
    file1.writelines(lines)
    file1.close()

# Get all grid squares which belong to top quintile of each column
top = data_q.apply(lambda x: x[x == x.max()], axis = 0)

# Join with original grid IDs and re-set index
top = pd.merge(pd.DataFrame(data[group_column]), top, left_index=True, right_index = True, how ='left')
top.set_index(group_column, drop=True, inplace =True)

#conver to binary 1 0
top = top.notnull().astype('int')

# Save spatial layer with binary labels for top quantile
top_geo = data[[group_column, "geometry"]].merge(top, left_on = group_column, right_index = True)
top_geo.to_file(os.path.join(datadir, r'urbangreens_grid.gpkg'), layer = quantilelayername, driver="GPKG")

#------------------------------
# CALCULATE JACCARD
#-------------------------------

# list column values (NOTE! these should only contain columns with actual data, not eg. id values..)
data_names = list(top.columns.values)

#Create output matrix for the results
jaccard_results = pd.DataFrame(index=data_names, columns = data_names)

# For each pair of data, calculate intersection, union and intersection over union...
for name1 in data_names:
    for name2 in data_names:

        intersection = len(top[(top[name1] == 1) & (top[name2] == 1)])
        union = intersection + len(top[(top[name1] == 0) & (top[name2] == 1)]) + len(top[(top[name1] == 1) & (top[name2] == 0)])
        jaccard = intersection / union

        print("Pairwise comparison of", name1, name2)
        print("Intersection:", intersection)
        print("Union:", union)
        print("Jaccard:", jaccard, "\n")

        jaccard_results.at[name1, name2] = jaccard

jaccard_results.to_csv(out_fp)
print("Saved output", out_fp)

"""
# Creating quintiles one-by one: 
pd.qcut(data['ZROP H17'],q=10, duplicates="drop").value_counts()
pd.qcut(data['insta_user'],q=10, duplicates="drop").value_counts()
pd.qcut(data['insta_gree'],q=10, duplicates="drop").value_counts()
pd.qcut(data['flickr_use'],q=10, duplicates="drop").value_counts()
pd.qcut(data['ZROP H17'],q=10, duplicates="drop").value_counts()

pd.qcut(data['insta_user'],q=10, duplicates="drop", labels = range(0, len(pd.qcut(data['insta_user'],q=10, duplicates="drop").value_counts())))
pd.qcut(data['insta_gree'],q=10, duplicates="drop")
pd.qcut(data['flickr_use'],q=10, duplicates="drop")
pd.qcut(data['ZROP H17'],q=10, duplicates="drop")
"""
