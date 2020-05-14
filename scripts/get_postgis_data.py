"""
This script reads in original social media data from PostGIS database on a server, and stores relevant data to
geopackage locally. 

# Input point layers collected from social media API's for the Helsinki Region
- Instagram
- Flickr
- Twitter

# output:
- points from helsinki stored as layers in a geopackage

RUN:
one input layer at a time.. It takes a while for Instagram due to big size of input database.


"""
import psycopg2
import geopandas as gpd
import os
import pandas as pd

def get_connection(db, user, host, port, password):
    # Create connection syntax
    session = "dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (db, user, host, port, password)
    try:
        conn = psycopg2.connect(session)
        print("Connection OK!")
    except:
        return print("Unable to connect to the database")
    return conn

def ask_database_details():
    # Input for db connection:
    db = input("Database: ")
    user = input("Database username: ")
    password= input("Password for user: " + user + " ")

    return db, user, password


if __name__ == "__main__":
    # MODIFY INPUT / OUTPUT HERE:

    outfolder = r"P:\h510\some\data\finland\vihersome_temp"

    # SET DATA SOURCE HERE:
    table = "twitter_in_hki" #"flickr_data_hki" #"instagram_data_helsinkiregion"
    
    # SET TIME RANGE HERE:
    timerange = "'2017-01-01' and '2017-12-31'"#"'2015-01-01' and '2015-12-31'"

    # CREATE QUERY FOR POSTS IN HELSINKI (the database also contains a polygon of Helsinki)
    if table.startswith("twitter"):
        columns = "{0}.id, {0}.userid, {0}.text, {0}.time_local, {0}.location_name, {0}.geom".format(table)
        timerange = "'2017-01-01' and '2017-12-31'"
        year = "2017"
    else:
        columns = "{0}.id, {0}.userid, {0}.text, {0}.time_local, {0}.photoid, {0}.photourl, {0}.location_name, {0}.geom".format(table)
        timerange = "'2015-01-01' and '2015-12-31'"
        year = "2015"

    query = """
        SELECT {1} 
        FROM {0}, helsinki_wgs84_poly
        WHERE ST_intersects({0}.geom, helsinki_wgs84_poly.geom) and TIME_LOCAL BETWEEN {2};
        """.format(table, columns, timerange)

    # Get user input for database details
    db, user, password = ask_database_details()

    #use database-functions for fetching the query
    conn = get_connection(db=db, user=user, host='localhost', port='3333', password=password)

    # fetch data to geodataframe
    print("Fetching data from table", table, "...")
    df = gpd.GeoDataFrame.from_postgis(query, conn)
    #greens = gpd.GeoDataFrame.from_postgis(query, conn)

    print("Saving", len(df), "records to geodatabase ...")
    df.to_file(os.path.join(outfolder, "urbangreens.gpkg"), layer=table[:5] + "_helsinki_" + year, driver="GPKG")
