import geopandas as gpd
import pandas as pd
import psycopg2
import os


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

# GROUP BY TIMEWINDOW
def make_timegrouped_query(edges, time_unit="WEEK"):
    """ Group strava data by time unit. Options: HOUR, DOY, WEEK, MONTH, ISODOW....."""
    query = """ SELECT  EXTRACT({0} from datetime),
                        COUNT(*) as row_count,
                        SUM(total_activity_count) as sum_tot_activity,
                        SUM(athlete_count) as sum_athletes,
                        SUM(commute_count) as sum_commute,
                        SUM(total_activity_count - commute_count) as sum_leisure_activity
                FROM hki15_edges_ride_data
                WHERE edge_id IN {1}
                GROUP BY EXTRACT({0} from datetime)
                ORDER BY EXTRACT({0} from datetime)""".format(time_unit, edges)

    return query


"""
# Query for fetching data for summer weekdays
"""
# query ="""SELECT   edge_id,
#            SUM(total_activity_count) as activity_sum,
#           SUM(athlete_count) as athlete_sum,
#            SUM(commute_count) as commute_sum,
#            SUM(total_activity_count - commute_count) as leisure_sum
#    FROM hki15_edges_ride_data
#    WHERE   EXTRACT(dow from datetime) in (1,2,3,4,5)
#            and datetime > '2015-05-01' and datetime < '2015-09-01'
#            and edge_id in {0}
#    GROUP BY edge_id
# """.format(time_unit, green_edges)


if __name__ == "__main__":

    # Open file created in QGIS (edges that intersect the YLRE green areas)
    fp=r"P:\h510\some\data\finland\vihersome_temp\Strava_edges_intersecting_vistracentroid_grids.shp"
    data = gpd.read_file(fp)

    time = "ISODOW"

    # list edge ids into a tuple
    data.columns.values
    green_edges = tuple(data.ID.unique())

    # Get user input for database details
    db, user, password = ask_database_details()

    # use database-functions for fetching the query
    conn = get_connection(db=db, user=user, host='localhost', port="3333", password=password)

    # Create query
    time_query = make_timegrouped_query(edges=green_edges, time_unit=time)

    # Fetch data from database using the connection and query
    grouped = pd.read_sql_query(time_query, conn)

    # Save query output
    datadir = r"P:\h510\some\data\finland\vihersome_temp"
    outfilename = "strava_%s.csv" % time
    grouped.to_csv(os.path.join(datadir, outfilename))
