"""
Plot treemap visualization of classified social media content

TODO: clean up messy code..

"""

# libraries
import matplotlib
import matplotlib.pyplot as plt
import squarify  # pip install squarify (algorithm for treemap)
import numpy as np
# If you have a data frame?
import pandas as pd


def plot_treemap(df, value_col, label_col, alpha = .8, figsize=(10, 20)):
    plt.figure(figsize=figsize)

    cmap = matplotlib.cm.Greens
    mini = min(df[value_col])
    maxi = max(df[value_col])
    norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in df[value_col]]

    t = squarify.plot(sizes=df[value_col], label=df[label_col], alpha=alpha, color=colors)
    plt.axis('off')

    return t


insta_fp = r"P:\h510\some\data\finland\social_media\instagram\content_analysis\Helsinki\Instagram2015_Helsinki_greenareas_classified_2019.pkl"
flickr_fp = r"P:\h510\some\data\finland\social_media\flickr\content_analysis\flickr_OSMGreen_Classified1843_2019.csv"

layers = {"Instagram": insta_fp,
              "Flickr": flickr_fp}

for layername, fp in layers.items():

    if layername == "Instagram":
        df = pd.read_pickle(fp)

        # Clean up the input-file
        df.replace({-1: 1}, inplace=True)
        df.replace({np.nan: 0}, inplace=True)

    if layername == "Flickr":
        df = pd.read_csv(flickr_fp, sep=",")
        df = df.replace({False:0, True:1})

    #UPDATE WINTER SPORTS
    #df[df["WinterSports"]==1].Comment_.value_counts()
    df['WinterSports'] = df.apply(lambda x: 1 if x["Skating"] == 1 else x['WinterSports'], axis =1)
    df['WinterSports'] = df.apply(lambda x: 1 if x["Skiing"] == 1 else x['WinterSports'], axis =1)

    # RE-CLASSIFY ACTIVITIES :
    # OTHER SPORTS df[df["OtherSports"]==1].Comment_.value_counts()

    # FISHING INTO WATER ACTIVITIES
    df['WaterSports'] = df.apply(lambda x: 1 if x["Comment_"] in ["fishing"] else x['WaterSports'], axis=1)


    # OTHER SPORTS, grouped
    #File1["other sports"] = File1["Comment_"].apply(lambda x: 1 if x in list2 else 0)

    # OTHER, not so sportive activities
    if layername == "Instagram":
        df['OtherActivity'] = df.apply(lambda x: 1 if x["Walking"] == 1 else x['OtherActivity'], axis =1)

        # Create separate field for ball games, and set these rows zero in "other sports" -column to prevent double counting
        list3 = ['football','sählyä ulokona', 'koripalloa kentällä','beach volley', 'handball','baseball', 'finnish baseball', 'tennis', 'basketball']
        df["ball games"] = df["Comment_"].apply(lambda x: 1 if x in list3 else 0) # FOR INSTA

        for activity in list3:
            df["OtherSports"] = df.apply(lambda x: 0 if x["Comment_"] == activity else x["OtherSports"], axis=1)

        actcol = ['DogWalking', 'Jogging', 'Biking',
               'WaterSports', 'WinterSports', 'Food_Drink',
               'Horseback_riding', 'Golf', 'Swimming', 'AdventurePark',
                 'OtherActivity','ball games',
                'OtherSports']

    if layername == "Flickr":
        actcol = ['DogWalking', 'Jogging', 'Biking',
               'WaterSports', 'WinterSports', 'Food_Drink',
               'Horseback_riding', 'Golf', 'Swimming', 'AdventurePark',
                'OtherSports']

    # Sum posts per activity (result has as many rows as there are activities in actcol)
    Act = df[actcol]
    sums = pd.DataFrame(Act.sum(), columns = ["sum"])
    sums["Activity"] = sums.index

    if layername == "Instagram":

        labels = {
            'DogWalking': 'dog walking',
            'Jogging': 'jogging',
            'Biking': 'cycling',
            'WinterSports': 'winter activities \n (cross-country skiing, \n ice-skating, sledding) ',
            'Food_Drink': 'eating/drinking',
            'Golf': 'golf',
            'Horseback_riding' : 'horse riding',
            'WaterSports': '\nwater activities \n (SUP, fishing,  \n kayaking)',
            'Skiing': 'cross-country skiing',
            'Swimming': 'swimming',
            'AdventurePark': 'Organized \n tree-climbing \n',
            'OtherSports' : 'other \n outdoor sports \n (workout, \n frisbeegolf, \n orienteering)',#INSTA
            'OtherActivity': 'other \n outdoor activities \n (walking around, \ngardening, dancing)',}

    if layername == "Flickr":
        labels = {
            'DogWalking': 'dog walking',
            'Jogging': 'jogging',
            'Biking': 'bicycling',
            'WinterSports': 'winter activities \n (cross-country skiing, \n ice-skating, sledding) ',
            'Food_Drink': 'eating/drinking',
            #'Skating': 'ice-skating',
            'Golf': 'golf',
            'Horseback_riding' : 'horse riding',
            #'orienteering': '\n orienteering',
            'Walking': 'walking',
            'WaterSports': '\nwater activities \n (SUP, fishing,  \n kayaking)',
            'Skiing': 'cross-country skiing',
            'Swimming': 'swimming',
            'AdventurePark': 'Organized \n tree-climbing \n',
            'OtherSports' : 'other \n outdoor sports', #FLICKR
            'OtherActivity': 'other \n outdoor activities \n (walking around, \ngardening, dancing)',}

    # Re-label activity names in activity-column
    sums.replace({"Activity": labels}, inplace = True)

    # Plot treemap
    plot_treemap(sums[sums["sum"]>0],  "sum", "Activity", alpha = 1, figsize= (8,30))
    plt.title(layername, size=24)

    plt.savefig(r"fig\%s_treemap.svg" % layername, format = "svg")
    plt.savefig(r"fig\%s_treemap.png" % layername, format="png")
    print("saved output for %s" % layername)
    #squarify.plot(sizes=df[value_col], label=df[label_col], alpha=.8)