""""
Script for plotting venn-diagrams based on classified social media data

Input:
    tabular data (read into Pandas) that has a binary classification for activities per post

Output:
    figure with a 3 -set venn-diagram

"""

from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles
import numpy as np
import pandas as pd


def plotvenn3(df, var1, var2, var3):
    """ Plot venn diagram  with 3 sets based on 3 columns of a Pandas DataFrame
        Based on:
            https://github.com/konstantint/matplotlib-venn
            http://matthiaseisen.com/pp/patterns/p0145/
    """
    plt.figure(figsize=(10, 10))
    set1 = set(df[df[var1] == 1].index)
    set2 = set(df[df[var2] == 1].index)
    set3 = set(df[df[var3] == 1].index)

    total = len(set1.union(set2.union(set3)))
    print(total)
    v = venn3(subsets=[set1, set2, set3], set_labels=(var1, var2, var3), subset_label_formatter=lambda x: '%0.0f%%' % (100*x/total))

    return v


def set_venn_colors(v, colorlist = ['#76a21e','#c6cf65', '#560d0d', "#f3ff93"]):
    """set colors for venn diagram subsets"""
    v.get_patch_by_id('100').set_color(colorlist[0])
    v.get_patch_by_id('110').set_color(colorlist[1])
    v.get_patch_by_id('111').set_color(colorlist[2])
    v.get_patch_by_id('101').set_color(colorlist[3])


def remove_irrelevant(df):
    df = df[df["NotAvailable"] == 0]
    df = df[df["NotRelevant"] == 0]

    return df

renamings = {"IndoorExperience": "Indoor",
            "GreenArea": "Green area photos",
            "Landscape": "Landscape photos",
            "Activity": "Activities"}

insta_fp = r"P:\h510\some\data\finland\social_media\instagram\content_analysis\Helsinki\Instagram2015_Helsinki_greenareas_MAR2019_classifiedOK.csv"
flickr_fp = r"P:\h510\some\data\finland\social_media\flickr\content_analysis\flickr_OSMGreen_Classified1843_2019.csv"


layers = {"Instagram": insta_fp,
              "Flickr": flickr_fp}


for layername, fp in layers.items():

    if layername == "Instagram":
        df = pd.read_csv(fp)
        df.replace({-1:1},inplace = True)
        df.replace({np.nan:0}, inplace = True)
        df.rename(columns=renamings, inplace=True)

    if layername == "Flickr":
        df = pd.read_csv(flickr_fp, sep=",")
        df.replace({False:0, True:1},inplace = True)
        df.replace({np.nan:0}, inplace = True)
        df.rename(columns=renamings, inplace=True)

    print(layername, "\n")
    print("df original length:", len(df))


    # DATA QUALITY CHECK 
    v = plotvenn3(df, 'NotRelevant', 'NotAvailable', "Green area photos")
    
    v.get_patch_by_id('100').set_color('lightgray')
    v.get_patch_by_id('010').set_color('gray')
    v.get_patch_by_id('001').set_color("green")

    #SET FONTSIZE FOR LABELS
    for text in v.set_labels:
        text.set_fontsize(24)

    #Subset label size
    for text in v.subset_labels:
        if text != None:
            text.set_fontsize(20)

    plt.title(layername + ", n=" + str(len(df)), fontsize=40)
    plt.savefig(r"fig\%s_venn_data_quality.svg" % layername, format="svg")
    plt.savefig(r"fig\%s_venn_data_quality.png" % layername, format="png")

    # REMOVE NOT RELEVANT AND UNAVAILABLE DATA
    df = remove_irrelevant(df)

    print("df length after removing irrelevant:", len(df))
    print(" df length of green area photos", len(df[df["Green area photos"] == 1]))

    # PLOT VENN DIAGRAM OF CONTENT TYPES
    v = plotvenn3(df, "Green area photos",  'Activities','Landscape photos')

    # SET SUBSET COLORS
    set_venn_colors(v, colorlist = ['#76a21e','#c6cf65', '#560d0d', "#f3ff93"])
    #colorlist = ['lightgreen','yellowgreen','darkgreen',"olive","wheat"]

    #SET FONTSIZE FOR LABELS
    for text in v.set_labels:
        text.set_fontsize(24)

    #Subset label size
    for text in v.subset_labels:
        if text != None:
            text.set_fontsize(20)

    plt.title(layername + ", n=" + str(len(df[df["Green area photos"] == 1])), fontsize=40)

    plt.savefig(r"fig\%s_venn.svg" % layername, format = "svg")
