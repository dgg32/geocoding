import googlemaps
from datetime import datetime
import os
import yaml
import pandas as pd
import numpy as np
from itertools import combinations
import mpu


with open("config.yaml", "r") as stream:
    try:
        PARAM = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


gmaps = googlemaps.Client(key=PARAM["GOOGLE_API_KEY"])

addresses = pd.read_csv("address.tsv", sep="\t")

for index, row in addresses.iterrows():
    geocode_result = gmaps.geocode(row["address"]) 
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]

    addresses.loc[index, "lat"] = lat
    addresses.loc[index, "lng"] = lng

idxs = list(combinations(addresses.index,2))
dfx = pd.DataFrame(np.concatenate((addresses.iloc[idx[0]].values, addresses.iloc[idx[1]].values)) for idx in idxs)
dfx.columns = ['s_name', 's_address', 's_lat', 's_lng', 'd_name', 'd_address', 'd_lat', 'd_lng']

for index, row in dfx.iterrows():
    dist = mpu.haversine_distance((row["s_lat"], row["s_lng"]), (row["d_lat"], row["d_lng"]))
    dfx.loc[index, "distance"] = dist

dfx[dfx["distance"] < 0.05]