"""
Script for calculating the Jaccard index between the top 10 % spatial
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

#-----------------------------
# Read input data
#------------------------------

#set output
out_fp = r"jaccard_results_inside_vistra.csv"

# input data
"""
fp = r"D:/ViherSOME/Data/YKR_grid/YKR_250m_mobilebigdata.shp"
data = gpd.read_file(fp)
"""


fp = "C:\LocalData\VUOKKHEI\codes\ViherSoMe\YKR_GreenCentroid_SpatialBigData.pkl"
data = pd.read_pickle(fp)

#check input data
data.head()
data.columns.values

# Replace zero with nan to exclude from classification
data.replace(to_replace=0, value=np.nan, inplace=True)

#select only needed columns (NOW THESTING WITH A LIMITED SET..)
data_values = data[['insta_userdays', 'insta_users',
       'flickr_userdays', 'flickr_users', 'instaf_userdays',
       'instaf_users', 'PPGISpark_user', 'PPGIS2050_user', 'ZROP H0',
       'ZROP H13', 'ZROP H14', 'ZROP H15', 'ZROP H16', 'ZROP H17',
       'ZROP H18', 'ZROP H20', 'ZROP H22']]

#------------------------------
# Get top 10 % of each column
#------------------------------

# Discretize column values (axis = 0) into 10 equal-sized buckets; output as bins
#https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.qcut.html
#data_q = data_values.apply(lambda x: pd.qcut(x, q=10, duplicates="drop"), axis = 0)

# Discretize column values (axis = 0) into 10 equal-sized buckets; output as flexible-length labels
data_q = data_values.apply(lambda x: pd.qcut(x,
                                             q=10,
                                             duplicates="drop",
                                             labels = range(0, len(pd.qcut(x,q=10, duplicates="drop").value_counts()))),
                                             axis = 0)

# Get all grid squares which belong to top quintile of each column
top10 = data_q.apply(lambda x: x[x==x.max()], axis = 0)

# Join with original grid IDs and re-set index
top10 = pd.merge(pd.DataFrame(data["YKR_ID"]), top10, left_index=True, right_index = True, how = 'left')
top10.set_index("YKR_ID", drop=True, inplace =True)

#conver to binary 1 0
top10 = top10.notnull().astype('int')

#------------------------------
# CALCULATE JACCARD
#-------------------------------

# list column values (NOTE! these should only contain columns with actual data, not eg. id values..)
data_names = list(top10.columns.values)

#Create output matrix for the results
jaccard_results = pd.DataFrame(index=data_names, columns = data_names)

# For each pair of data, calculate intersection, union and intersection over union...
for name1 in data_names:
    for name2 in data_names:

        intersection = len(top10[(top10[name1]==1) & (top10[name2]==1)])
        union =  intersection + len(top10[(top10[name1]==0) & (top10[name2]==1)]) + len(top10[(top10[name1]==1) & (top10[name2]==0)])
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
