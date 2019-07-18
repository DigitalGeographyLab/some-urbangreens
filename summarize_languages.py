""""
This script summarizes identified languages per user per polygon

1. Identify language per user based on the whole data
- if users has used more than 1 language,
    first remove english, then select the most frequently used language

2. Summarize languages per polygon
- ignore languages used by less than 10 users (to avoid false positive random languages)


Disclaimer: A bit heavy and long script.. step 1 is a bit slow but works :)

"""
import geopandas as gpd
import pandas as pd
import itertools
from matplotlib import pyplot as plt


def define_language(users_langs):
    """
    Define which language to pick from a list/series of languages

    Handles cases when length of language list is 0, 1 or > 1.
    If there are > 1 languages, first remove English (if present), then select the most used language.

    :param languages: list or pd.Series containing languages
    :return: str language code
    """
    # drop duplicates from input list/series
    users_langset = set(users_langs)

    # If no languages detected:
    if len(users_langset) == 0:
        lan = None

    elif len(users_langset) == 1:
        # if there is only one
        lan = users_langset.pop()

    # If more than one language
    elif len(users_langset) > 1:

        # If English, remove it from full list
        if 'en' in users_langset:
            users_langs = users_langs[users_langs != 'en']

        # get the language that the user has used the most
        # if after removing English there is only one language, it gets chosen here
        lan = users_langs.value_counts().idxmax()

    return lan


def get_users_language(df, usercol ="userid"):
    """
    Group dataframe by user id and get the primary language for each user (using another function).
    """
    # if multiple users, this is makes sure
    resultdf = pd.DataFrame(index = df[usercol].unique())
    resultdf["language"] = ""

    users = df.groupby(usercol)

    for key, usersposts in users:
        # chain languages (ignores empty language lists, and gives unique index for all items.)
        users_langs = pd.Series(itertools.chain(*usersposts.langs))

        lan = define_language(users_langs)

        # Add user's language to result df
        resultdf.at[key, "language"] = lan

    return resultdf


def plot_top_langs(values, n = 10, title = "x"):
    """ Plot users per language in a bar graph"""
    ax = values.head(n).sort_values(ascending=True).plot.barh(color="black")
    plt.title(title, fontsize=24)
    ax.set_ylabel("Language", fontsize=16)
    ax.set_xlabel("users", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=14)

    plt.savefig(r"fig\language_usercounts_%s.png" % title)
    plt.savefig(r"fig\language_usercounts_%s.svg" % title)

#---------------------------
# Input data
#---------------------------

# Social media points, takes a while to read..
points = pd.read_pickle(r"P:\h510\some\data\finland\social_media\instagram\languages\instagram_Helsinki_fasttext_parsed_geom.pkl")
points = gpd.GeoDataFrame(points, geometry = "geom")
points.crs = {'init': 'epsg:4326'}

# Make sure there are no duplicates
points.drop_duplicates(subset="photoid", inplace = True)

# polygons:
poly_fp = r"P:\h510\some\data\finland\gis_layers\VISTRA\VISTRA_vihersormet_epsg3047_fixed_geom.shp"
poly = gpd.read_file(poly_fp)
poly_id = "id_right" # 595 unique values in the green finger layer

file_id = "green_fingers"

# OPTION 2: YKR grid polygons:
#grid_fp = r"P:\h510\some\data\finland\gis_layers\VISTRA\YKR_250m_Helsinki_centroidin_VISTRA_Vihersormi_fixedgeom.shp"
#poly = gpd.read_file(grid_fp)
#poly_id = "GRIDCODE"
#file_id = "YKR_grid"

print("input data ok")

#-----------------------------------
# language summary for whole data
#-----------------------------------

#Convert language set to lists:
#points["langs"] = points["langs"].apply(lambda x: list(x))

# Define language for each user:
userlangs = get_users_language(points)

# summarize users per language
toplangs_helsinki = userlangs.language.value_counts()

# save summary
toplangs_helsinki.to_csv(r"lang_results\Instagram_languages_usercounts_helsinki.csv")

# plot summary
plot_top_langs(toplangs_helsinki, n = 10, title = "Helsinki")

#---------------------------
# Languages in parks
#-----------------------------

if points.crs != poly.crs:
    print("CRS do not match")
    print("reprojecting the first layer to", str(poly.crs))
    points = points.to_crs(poly.crs)

# Inner spatial join between points and polygons:
# result contains points intersecting
greenpoints = gpd.sjoin(points, poly, how='inner', op="intersects")

# Make sure there are no duplicates
greenpoints.drop_duplicates(subset="photoid", inplace = True)

# add users lang info
greenpoints = greenpoints.merge(userlangs, left_on = "userid", right_index = True)

# summarize users per language
greenusers = greenpoints.drop_duplicates(subset = "userid")
toplangs_parks = greenusers.language.value_counts()

#save summary for languages used by at least 10 users
toplangs_parks[toplangs_parks > 10].to_csv(r"lang_results\Instagram_languages_usercounts_greens_%s.csv" % file_id)

# plot summary
plot_top_langs(toplangs_parks, n = 10, title = "Greens %s" % file_id)

# list languages with more than 10 users
lanlist = toplangs_parks[toplangs_parks > 10].index

# Set languages used by less than 10 as None
greenpoints["language"] = greenpoints['language'].apply(lambda x: x if x in lanlist else None)

print("ignored languages with less than 10 users")

#-------------------------
# Final park summary
#------------------------

# group data by polygon id
grouped = greenpoints.groupby(by = poly_id)

# Data frame for storing the output
parks = pd.DataFrame()

for park_id, group in grouped:

    # get languages used in park into a data frame
    # rows: park id, columns: languages
    langs_in_park = group.language.value_counts()
    languages = pd.DataFrame(langs_in_park).transpose()
    languages.index = [park_id]

    # Concatenate to existing result (if new languages appear, new column appears..)
    parks = pd.concat([parks, languages], sort = False)

# Count distinct languages in each park
parks["lang_count"] = parks.apply(lambda x: x.count(), axis = 1)

# store park id in column
parks["park_id"] = parks.index

# number of posts and users
parks["users"] = greenpoints.groupby(by=poly_id).userid.nunique()
parks["posts"] = greenpoints.groupby(by=poly_id).photoid.nunique()

#Save output
parks.to_csv(r"lang_results\parks_users_language_counts_%s.csv" % file_id)

