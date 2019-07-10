"""Script for plotting temporal graphs from strava data

#Input
- csv file with Strava data grouped by time unit

# output
- temporal plot .png -file

"""
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_temporal(df, columns=['sum_tot_activity', 'sum_leisure_activity'], time = "day of week"):
    """"plot time on x axis and share of data per time unit on y axis"""
    ax = df[columns].plot(xticks=df.index, style=['o-k', 's-g', '^-b'])
    #ax.legend(["all activities", "commute activities", "non-commute activities"])
    ax.set_ylabel("share of all activities", fontsize = 16)
    ax.set_xlabel(time, fontsize = 16)
    ax.set_xticklabels(df.index + 1, fontsize = 12)

    return ax


# Normalize columns (pattern is the same, but Y-axis is more legible
def normalize_column(df, column, tot_column):
    """calculates share of all users per time unit"""
    normalized = df.apply(lambda x: x[column]/df[tot_column].sum(), axis = 1)
    return normalized


#Input data
time = "HOUR"
datadir = r"P:\h510\some\data\finland\vihersome_temp"
filename = "strava_%s.csv" % time
strava = pd.read_csv(os.path.join(datadir, filename))

#normalize columns
strava["all_norm"] = normalize_column(strava, "sum_tot_activity","sum_tot_activity")
strava["leisure_norm"] = normalize_column(strava, "sum_leisure_activity","sum_tot_activity")
strava["commute_norm"] = normalize_column(strava, "sum_commute","sum_tot_activity")

# set font sizes
plt.style.use('seaborn-whitegrid')
#fig, ax = plt.subplots() #fig, ax = plt.subplots(figsize=(20,10))
plt.rc('legend', fontsize=14)  # legend fontsize

#Plot
ax = plot_temporal(df=strava, columns=["all_norm","commute_norm", "leisure_norm"], time = "hour")

#FINALIZE FIGURE:
plt.gca().get_lines()[0].set_color('0')
plt.gca().get_lines()[1].set_color("0.6")
plt.gca().get_lines()[2].set_color("0.4")

ax.legend(["all activities", "commute", "leisure"])

#plt.yticks(np.arange(0.00, 0.20, step=0.02))

#fix y ticks to match the strava plot
plt.yticks(np.arange(0.00, 0.12, step=0.02))

# tick font
plt.tick_params(axis='both', which='major', labelsize=12)

# save
plt.savefig(r"fig\strava_%s.png" % time)