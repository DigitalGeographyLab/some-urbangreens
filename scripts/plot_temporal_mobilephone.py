""" Script for plotting the temporal graphs for mobile phone data"""

import geopandas as gpd
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def calculate_share(df, timecols):
    """Calculate hourly share of activity"""
    hourly = pd.DataFrame(df[timecols].sum(), columns=["sum"])
    hourly["share"] = hourly["sum"] / hourly["sum"].sum()

    return hourly


def plot_temporal_share(df, style = 'o-k'):
    """Plot temporal graph"""

    ax = df["share"].plot(style=style)
    plt.xticks(np.arange(0, 24, 1.0))

    return ax

# Set layer name and time interval
layer = "greengrid"
time = "hour"

# input data
datadir = r"P:\h510\some\data\finland\vihersome_temp"
data = gpd.read_file(os.path.join(datadir, r'urbangreens_grid.gpkg'), layer=layer)

# list column names
timecols = ['ZROP H1', 'ZROP H2', 'ZROP H3',
       'ZROP H4', 'ZROP H5', 'ZROP H6', 'ZROP H7', 'ZROP H8', 'ZROP H9',
       'ZROP H10', 'ZROP H11', 'ZROP H12', 'ZROP H13', 'ZROP H14',
       'ZROP H15', 'ZROP H16', 'ZROP H17', 'ZROP H18', 'ZROP H19',
       'ZROP H20', 'ZROP H21', 'ZROP H22', 'ZROP H23', 'ZROP H0']

# Initiate plot
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()

# set font sizes
plt.rc('legend', fontsize=14)  # legend fontsize

# ticks
plt.yticks(np.arange(0.00, 0.12, step=0.02))
plt.tick_params(axis='both', which='major', labelsize=12)

# ALL GREEN GRID SQUARES
share = calculate_share(data, timecols)
plot_temporal_share(share, style = 'o-k')

# KESKUSPUISTO ONLY
hourly_kpuisto =  calculate_share(data[data["YKR_ID"]==5902057], timecols)
plot_temporal_share(hourly_kpuisto, style ='s-g')

# line styles
plt.gca().get_lines()[0].set_color("0")  # black
plt.gca().get_lines()[1].set_color("0.6")  # darker grey

plt.legend(["in all green space grids", "in central park grid"])
ax.set_ylabel("hourly share of mobile phone data")

plt.yticks(np.arange(0.00, 0.12, step=0.02))
#ax.set_yticklabels(np.arange(0, 0.12, step=0.02))

ax.set_xticklabels(np.arange(1, 25, step=1))
ax.set_xlabel(time)

plt.savefig(r"fig\mobile_phone_%s.png" % time)