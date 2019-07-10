"""
Plot temporal (hour/month/week/..)graphs from social media data. Eg. share of all users across all months.
requires a column "time_local" with timestamp, and "userid" -column with unique user id.

TODO: clean up functions..
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os

def groupbytime(somedata, time):
    """
    Group input dataframe based on hour and calculate count of photos, users and photos per user per hour
    # could try: df.groupby(df.index.to_period('T'))
    """
    # Group data based based on time unit

    if time == "hour":
        grouped = somedata.groupby(lambda x: x.hour)

    elif time == "dayofyear":
        grouped = somedata.groupby(lambda x: x.dayofyear)

    elif time == "week":
        grouped = somedata.groupby(lambda x: x.week)

    elif time == "dayofweek":
        grouped = somedata.groupby(lambda x: x.dayofweek)

    elif time == "month":
        grouped = somedata.groupby(lambda x: x.month)

    return grouped


def getcounts(grouped_data):
    """ """

    #Extract count of photos and users per hour into a dataframe
    counts = pd.DataFrame()
    #counts['photos'] = grouped_data.photoid.nunique()
    counts['users'] = grouped_data.userid.nunique()
    #counts['photoperuser'] = counts['photos'] / counts['users']

    #proportional user count
    #counts['prop_users'] = counts['users'] / counts['users'].sum()

    return counts


def normalize_couts(counted_data, time):
    """ """

    #get counts for the whole data:
    time_counts = getcounts(groupbytime(some, time))

    # Normalize
    normalized_counts = counted_data / time_counts

    return normalized_counts[["users"]]


def plot_counts(counts, time_unit, column="users", style='o-k'):
    """
    :param counts: Pandas DataFrame
    :param time_unit: string used as x axis label
    :param column: column to plot
    :param style: string for linestyle
    :return: plot object
    """
    # Plot photo count per hour
    ax = counts[column].plot(xticks=counts.index, style=style)
    ax.set_ylabel("share of all %s" % column, fontsize = 16)
    ax.set_xlabel(time_unit, fontsize = 16)

    return ax

if __name__ == "__main__":

    # Settings
    time = "hour"  #"month" #"week" #"hour" #"week" #"dayofweek"
    value = "users"

    # input data
    datadir = r"P:\h510\some\data\finland\vihersome_temp"

    # Dictionary contains info of layername: and its userid column name
    layers_usercols = {"insta_helsinki_2015_greens": 'userid',
                       "flick_helsinki_2015_greens": 'userid',
                       "twitt_helsinki_2017_greens": 'userid'}

    # labels for plotting
    labels = {"insta_helsinki_2015_greens": 'Instagram',
              "flick_helsinki_2015_greens": 'Flickr',
              "twitt_helsinki_2017_greens": 'Twitter'}

    # linestyle
    styles = {"insta_helsinki_2015_greens": 'o-k',
              "flick_helsinki_2015_greens": 's-g',
              "twitt_helsinki_2017_greens": '^-b'}

    # Define plot
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()

    # set font sizes
    plt.rc('legend', fontsize=14)  # legend fontsize
    # following: https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot

    for layer, user_column in layers_usercols.items():
        # Read in layer from geopackage
        df = gpd.read_file(os.path.join(datadir, r'urbangreens.gpkg'), layer=layer)

        #Set datetime index
        df = df.set_index(pd.DatetimeIndex(df["time_local"]))

        # Group by and normalize for time unit
        time_counts = getcounts(groupbytime(df, time))
        normalized_counts = time_counts / time_counts.sum()
        plot_counts(normalized_counts, time, value, style=styles.get(layer))

        #fix y ticks to match the strava plot

        #plt.yticks(np.arange(0.00, 0.20, step=0.02))
        #ax.set_xticklabels(normalized_counts.index + 1)

    # FINALIZE FIGURE:
    # line styles
    plt.gca().get_lines()[0].set_color("0")  # black
    plt.gca().get_lines()[1].set_color("0.6")  # darker grey
    plt.gca().get_lines()[2].set_color("0.4")  # lighter grey

    # legend
    plt.legend(list(labels.values()))

    # axes
    plt.yticks(np.arange(0.00, 0.12, step=0.02))
    ax.set_xticklabels(normalized_counts.index + 1)

    # tick font
    plt.tick_params(axis='both', which='major', labelsize=12)

    # save
    plt.savefig(r"fig\socialmedia_%s.png" % time)
