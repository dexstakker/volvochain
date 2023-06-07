import csv
import sys
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt

import psycopg
#import psycopg-binary
import json
# Note: the module name is psycopg, not psycopg3

# Connect to an existing database
with psycopg.connect("postgresql://postgres:postgres@192.168.1.159:2022/general") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        try:
            delete_table = "DROP TABLE gps_targets;"
            cur.execute(delete_table)
            conn.commit()
        except:
            print("Problems")
        finally:
            print("Tables cleared")

        #Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE gps_targets (
                id varchar(24),
                lon real,
                lat real)
            """)
        conn.commit()


        with open('data/GPS_track.json', 'r') as f:
            data = json.load(f)

        imu = 0
        pose = 0
        dflongitude = []
        dflatitude = []

        #print(len(data.keys()), " keys")
        ls = data.keys()
        with open('data/points.csv', 'w') as csvfile:
            fieldnames = ['id', 'lon', 'lat']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k in ls:
                nd = data[k]
                if 'pose' in nd:
                    pose = pose + 1
                    poseDict = nd['pose']
                    id = k
                    lon = poseDict['lon']
                    dflongitude.append(lon)
                    lat = poseDict['lat']
                    dflatitude.append(lat)
                    vals = (id, lon, lat)
                    writer.writerow({'id': id, 'lon': lon, 'lat':lat})
                    cur.execute(
                        "INSERT INTO gps_targets (id, lon, lat) VALUES (%s, %s, %s)", vals)
                    conn.commit()
            #print(pose, " poses found")
            BBox = (min(dflongitude), max(dflongitude),
                     min(dflatitude), max(dflatitude)   )
            print(BBox)
            #ruh_m = plt.imread('data/map.png')