# by Matias I. Bofarull Oddo - 2022.03.12

import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# https://www.pyrunner.com/weblog/2018/04/12/kalman-example/


def file_parser(txt_name):
    with open(txt_name, "r") as f:
        lines = f.read().splitlines()
        f.close()
    data_ts = []
    data_idx = []
    data_lat = []
    data_lon = []
    data_alt = []
    data_hac = []
    data_vac = []
    data_sql = []
    for line in lines:
        point = json.loads(line)
        if point["ts"] == "NaN":
            continue
        else:
            data_ts.append(datetime.fromtimestamp(int(point["ts"])))
            # data_ts.append(point["ts"])
            data_idx.append(point["idx"])
            data_lat.append(point["lat"])
            data_lon.append(point["lon"])
            data_alt.append(point["alt"])
            data_hac.append(point["hac"])
            data_vac.append(point["vac"])
            data_sql.append(point["sql"])
    return (
        data_ts,
        data_idx,
        data_lat,
        data_lon,
        data_alt,
        data_hac,
        data_vac,
        data_sql,
    )


def filter_sql(lat, lon, sql):
    event_lat = []
    event_lon = []
    for i, value in enumerate(sql):
        if value == 1:
            event_lat.append(lat[i])
            event_lon.append(lon[i])
    return event_lat, event_lon


###############################################################################

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)

ts, idx, lat, lon, alt, hac, vac, sql = file_parser(
    "data_tracks/SquirrelQuest_2023_03_11_15_07_34_0664_matt.txt"
)
ax.scatter(np.array(ts), np.array(sql), s=1, c="tab:blue")

ts, idx, lat, lon, alt, hac, vac, sql = file_parser(
    "data_tracks/SquirrelQuest_2023_03_11_15_07_34_2851_ying.txt"
)
ax.scatter(np.array(ts), np.array(sql), s=1, c="tab:green")

ts, idx, lat, lon, alt, hac, vac, sql = file_parser(
    "data_tracks/SquirrelQuest_2023_03_11_15_07_34_8461_bereket.txt"
)
ax.scatter(np.array(ts), np.array(sql), s=1, c="tab:red")

plt.show()

###############################################################################

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)

ts, idx, lat, lon, alt, hac, vac, sql = file_parser(
    "data_tracks/SquirrelQuest_2023_03_11_15_07_34_0664_matt.txt"
)

event_lat, event_lon = filter_sql(lat, lon, sql)
ax.plot(np.array(lon), np.array(lat), "-", linewidth=1, c="silver", zorder=0)
ax.scatter(np.array(event_lon), np.array(event_lat), s=5, c="tab:blue")

ts, idx, lat, lon, alt, hac, vac, sql = file_parser(
    "data_tracks/SquirrelQuest_2023_03_11_15_07_34_2851_ying.txt"
)

event_lat, event_lon = filter_sql(lat, lon, sql)
ax.plot(np.array(lon), np.array(lat), "-", linewidth=1, c="silver", zorder=0)
ax.scatter(np.array(event_lon), np.array(event_lat), s=5, c="tab:green")

ts, idx, lat, lon, alt, hac, vac, sql = file_parser(
    "data_tracks/SquirrelQuest_2023_03_11_15_07_34_8461_bereket.txt"
)

event_lat, event_lon = filter_sql(lat, lon, sql)
ax.plot(np.array(lon), np.array(lat), "-", linewidth=1, c="silver", zorder=0)
ax.scatter(np.array(event_lon), np.array(event_lat), s=10, c="tab:red")

ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
plt.show()

###############################################################################
