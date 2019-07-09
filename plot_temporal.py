"""
Plot temporal (hour/month/week/..)graphs from social media data. Eg. share of all users across all months.
requires a column "time_local" with timestamp, and "userid" -column with unique user id.

TODO: clean up functions..
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    #Extract count of photos and users per hour into a dataframe
    counts = pd.DataFrame()
    #counts['photos'] = grouped_data.photoid.nunique()
    counts['users'] = grouped_data.userid.nunique()
    #counts['photoperuser'] = counts['photos'] / counts['users']

    #proportional user count
    #counts['prop_users'] = counts['users'] / counts['users'].sum()

    return counts

def normalize_couts(counted_data, time):

    #get counts for the whole data:
    time_counts = getcounts(groupbytime(some, time))

    # Normalize
    normalized_counts = counted_data / time_counts

    #return normalized_counts[["photos", "users"]]
    return normalized_counts[["users"]]

def plotcounts(counts, time, topic="photos", value="users"):
    """

    :type counts: Pandas DataFrame
    """
    # Plot photo count per hour
    ax = counts[value].plot(xticks=counts.index, style=['o-k'])
    ax.legend([topic])
    ax.set_ylabel("share of all %s" % value)
    ax.set_xlabel(time)

    return ax

def plot_theme_normalized(db, topic, time, value):
    counts = getcounts(groupbytime(db[db[topic] == 1], time))
    normalized = normalize_couts(counts, time)
    ax = plotcounts(normalized, time, topic, value)

    return ax


if __name__ == "__main__":

    # Settings
    time ="hour" #"month"  # "week"#"hour" #"week"#"dayofweek" #
    value = "users"

    # input data
    datadir = r"P:\h510\some\data\finland\vihersome_temp"

    # List layers for analysis (these exist in the geodatabase
    # Dictionary contains info of layername: type
    layers = {"insta_helsinki_2015_greens": "socialmedia",
              "flick_helsinki_2015_greens": "socialmedia",
              "twitt_helsinki_2017_greens": "socialmedia"}

    # Dictionary contains info of layername: unique user id column
    usercolumns = {"insta_helsinki_2015_greens": 'userid',
                   "flick_helsinki_2015_greens": 'userid',
                   "twitt_helsinki_2017_greens": 'userid'}
    labels = {"insta_helsinki_2015_greens": 'Instagram',
                   "flick_helsinki_2015_greens": 'Flickr',
              "twitt_helsinki_2017_greens": 'Twitter'}

    # Define plot
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    plt.yticks(np.arange(0.00, 0.12, step=0.02))
    ax.set_xticklabels(normalized_counts.index + 1)

    for layer, usercolumn in usercolumns.items():
        # Read in layer from geopackage
        df = gpd.read_file(os.path.join(datadir, r'urbangreens.gpkg'), layer=layer)

        #Set datetime index
        df = df.set_index(pd.DatetimeIndex(df["time_local"]))

        # Whole data
        #fig, ax = plt.subplots()
        #time_counts = getcounts(groupbytime(df, time))
        #plotcounts(time_counts, time, value)

        #ax.set_ylabel(value)
        #plt.gca().get_lines()[1].set_color("green")
        #ax.legend([labels.get(layer)])

        time_counts = getcounts(groupbytime(df, time))
        normalized_counts = time_counts / time_counts.sum()
        plotcounts(normalized_counts, time, value)

        #fix y ticks to match the strava plot

        #plt.yticks(np.arange(0.00, 0.20, step=0.02))
        #ax.set_xticklabels(normalized_counts.index + 1)

    # FINALIZE FIGURE:
    plt.gca().get_lines()[0].set_color("black")
    plt.gca().get_lines()[1].set_color("grey")
    plt.gca().get_lines()[2].set_color("lightgrey")
    plt.yticks(np.arange(0.00, 0.12, step=0.02))
    ax.set_xticklabels(normalized_counts.index + 1)
    ax.legend(list(labels.values()))

    plt.savefig(r"fig\socialmedia_%s.png" % time)
"""

    
    plt.gca().get_lines()[2].set_color("red")
    plt.gca().get_lines()[3].set_color("orange")
    plt.gca().get_lines()[4].set_color("brown")

    ax.legend(topics)

"""