import geopandas as gpd
import pandas as pd
import itertools


def get_users_language(df, usercol ="userid"):

    users_langs = []
    users = df.groupby(usercol)

    for key, usersposts in users:
        users_langlist = list(itertools.chain(*usersposts.langs))
        users_langset = set(users_langlist)

        if len(users_langset) > 1:

            if 'en' in users_langset:
                users_langset.remove('en')

            if len(users_langset) > 1:
                if 'sv' in users_langlist:
                    users_langs.append(['sv'])
                elif 'fi' in users_langset:
                    users_langs.append(['fi'])
                elif 'ru' in users_langset:
                    users_langs.append(['ru'])
                elif 'ja' in users_langset:
                    users_langs.append(['ja'])
                elif 'no' in users_langset:
                    users_langs.append(['no'])
                elif 'es' in users_langset:
                    users_langs.append(['es'])
                elif 'ar' in users_langset:
                    users_langs.append(['ar'])
                elif 'de' in users_langset:
                    users_langs.append(['de'])

        else:
            users_langs.append(list(users_langset))

    users_langlist = list(itertools.chain(*users_langs))

    #convert to series to allow summaries
    users_langseries = pd.Series(users_langlist)

    return users_langseries



# INPUT DATA
data = pd.read_pickle(r"D:\CODES\ViherSoMe\languages\instagram_Helsinki_fasttext_parsed_geom.pkl")
points = gpd.GeoDataFrame(data, geometry = "geom")
points.crs =
#data= points_intersect
#del df

areacolumn = "name"
areacolumn = 'dissID_1'


greenfingers = gpd.read_file(r"D:\ViherSOME\Data\VISTRA\VISTRA_vihersormet_epsg3047.shp")


if data.crs != greenfingers.crs:
    print("CRS do not match:" + str(df1.crs) + "and" + str(df2.crs))
    print("reprojecting the first layer to", str(df2.crs))
    data = data.to_crs(greenfingers.crs)

data = gpd.sjoin(data, greenfingers, how='left',op="intersects")


# language summary for whole data
languages = get_users_language(data)
languages.value_counts().head(10).sort_values(ascending=True).plot.barh(color="black")


parks = pd.DataFrame()

# group data by area name

#Convert language set to lists:
data["langs"] = data["langs"].apply(lambda x: list(x))

grouped = data.groupby(by = areacolumn)
for parkname, group in grouped:

    # BASED ON POSTS
    #Flatten all languages in the area into one list
    # https: // stackoverflow.com / questions / 10424219 / combining - lists - into - one
    langlist = list(itertools.chain(*group.langs))

    #convert to series to allow summaries
    langseries = pd.Series(langlist)

    print("------------------------------")
    #print("###", parkname, "LANGS BASED ON POSTS###")
    #print(langseries.value_counts())

    #convert to series to allow summaries
    users_langseries = get_users_language(group)

    print("------------------------------")
    print("###", parkname, "LANGS BASED ON USERS ###")
    print(users_langseries.value_counts())

    languages = pd.DataFrame(users_langseries.value_counts()).transpose()
    languages.index = [parkname]

    parks = pd.concat([parks, languages])

# Finalize parks -dataframe

parks["lang_count"] = parks.apply(lambda x: x.count(), axis = 1)
parks["name"] = parks.index

parks["users"] = data.groupby(by=areacolumn).userid.nunique()
parks["posts"] = data.groupby(by=areacolumn).photoid.nunique()

parks.to_csv(r"parks_users_language_counts.csv")

