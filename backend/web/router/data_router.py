import json
import os
from copy import deepcopy
from datetime import timedelta, date
from typing import List, Dict, Union, Tuple

import matplotlib.path as mplPath
import numpy as np
import rootpath
from dateutil import parser
from flask import Blueprint, make_response, jsonify, send_from_directory, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import BOUNDARY_PATH

bp = Blueprint('data', __name__, url_prefix='/data')


def gen_date_series(days: int, timestamp_str: str) -> List[Tuple[date, None]]:
    _date = parser.parse(timestamp_str).date() - timedelta(days=days - 1)
    return [(_date + timedelta(days=i), None) for i in range(days)]


def fill_series(date_series: List[Tuple[date, None]], fill: List[Tuple[date, Union[int, float, None]]]) \
        -> List[Tuple[date, Union[int, float, None]]]:
    # noinspection Mypy
    result_series: List[Tuple[date, Union[int, float, None]]] = deepcopy(date_series)
    for fill_date, value in fill:
        for i, (tweet_date, _) in enumerate(result_series):
            if tweet_date == fill_date:
                result_series[i] = (tweet_date, value)
                break
    return result_series


@bp.route("/aggregation", methods=['POST'])
def aggregation():
    request_json = flask_request.get_json(force=True)
    lat = float(request_json['lat'])
    lng = float(request_json['lng'])
    radius = float(request_json['radius'])
    timestamp_str = request_json['timestamp']
    days = int(request_json.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

    query_tweet = 'SELECT * from aggregate_tweet(%s, %s, %s, TIMESTAMP %s, %s)'
    query2_temp = 'SELECT * from aggregate_temperature(%s, %s, %s, TIMESTAMP %s, %s)'
    query3_mois = 'SELECT * from aggregate_moisture(%s, %s, %s, TIMESTAMP %s, %s)'
    query4_ppt = '''
        select rft."date", avg(prism.ppt) from prism,
        (
            SELECT rft."date" from prism_info rft
            where rft."date" <= TIMESTAMP %s -- UTC timezong
            -- returning PDT without timezong label
            and rft."date" > TIMESTAMP %s - ( %s || ' day')::interval
        ) as rft,
        (
            select mesh.gid from us_mesh mesh 
            WHERE st_dwithin(st_makepoint(%s, %s),mesh.geom, %s)
        ) as gids
        where prism.gid=gids.gid
        and prism."date" = rft."date"
        and prism.ppt != FLOAT 'NaN'
        GROUP BY rft."date"
    '''
    with Connection() as conn:
        cur = conn.cursor()

        # tweet count from 'records'
        cur.execute(query_tweet, (lng, lat, radius, timestamp_str, days))  # lng lat +-180
        tweet = cur.fetchall()
        tweet_series = fill_series(date_series, tweet)
        # temp, mois from NOAA
        cur.execute(query2_temp, (lng, lat, radius, timestamp_str, days))
        temp = cur.fetchall()
        temp_series = fill_series(date_series, temp)
        cur.execute(query3_mois, (lng, lat, radius, timestamp_str, days))
        mois = cur.fetchall()
        mois_series = fill_series(date_series, mois)
        # ppt from PRISM
        cur.execute(query4_ppt, (timestamp_str, timestamp_str, days, lng, lat, radius))
        ppt = cur.fetchall()
        ppt_series = fill_series(date_series, ppt)
        resp = make_response(jsonify({'tmp': temp_series, 'soilw': mois_series, 'cnt_tweet': tweet_series,
                                      'ppt': ppt_series}))

        cur.close()
    return resp


@bp.route('region-temp', methods=['GET'])
def region_temp():
    region_id = int(flask_request.args.get('region_id'))
    timestamp_str = flask_request.args.get('timestamp')
    days = int(flask_request.args.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

    query = '''
    select date(rft.reftime), avg(tmp) from noaa0p25 noaa,
    (
        SELECT reftime, tid from noaa0p25_reftime rft
        where rft.reftime < TIMESTAMP '{timestamp}'
        and rft.reftime > TIMESTAMP '{timestamp}' - interval '{days} day'
    ) as rft,
    (
        SELECT geometry.gid from noaa0p25_geometry_neg geometry,
        (
            SELECT geom from us_states WHERE state_id={region_id}
            union
            SELECT geom from us_counties WHERE county_id={region_id}
            union
            SELECT geom from us_cities WHERE city_id={region_id}
        ) as region
        where st_contains(region.geom, geometry.geom)
    ) as gids
    where noaa.gid=gids.gid
    and noaa.tid = rft.tid
    GROUP BY date(rft.reftime)
    '''

    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query.format(region_id=region_id, timestamp=timestamp_str, days=days))
        resp = make_response(jsonify(
            fill_series(date_series, cur.fetchall())
        ))
    return resp


@bp.route('region-moisture', methods=['GET'])
def region_moisture():
    region_id = int(flask_request.args.get('region_id'))
    timestamp_str = flask_request.args.get('timestamp')
    days = int(flask_request.args.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

    query = '''
    select date(rft.reftime), avg(soilw) from noaa0p25 noaa,
    (
        SELECT reftime, tid from noaa0p25_reftime rft
        where rft.reftime < TIMESTAMP '{timestamp}'
        and rft.reftime > TIMESTAMP '{timestamp}' - interval '{days} day'
    ) as rft,
    (
        SELECT geometry.gid from noaa0p25_geometry_neg geometry,
        (
            SELECT geom from us_states WHERE state_id={region_id}
            union
            SELECT geom from us_counties WHERE county_id={region_id}
            union
            SELECT geom from us_cities WHERE city_id={region_id}
        ) as region
        where st_contains(region.geom, geometry.geom)
    ) as gids
    where noaa.gid=gids.gid
    and noaa.tid = rft.tid
    GROUP BY date(rft.reftime)
    '''

    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query.format(region_id=region_id, timestamp=timestamp_str, days=days))
        resp = make_response(jsonify(
            fill_series(date_series, cur.fetchall())
        ))
    return resp


@bp.route("/temp", methods=['POST'])
def temperature_in_screen():
    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    tid = request_json['tid']
    interval = request_json['interval']

    query = "SELECT * from Polygon_Aggregator_noaa0p25(%s, %s, %s)"
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(north, west, east, south)
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (poly, tid, interval))
        resp = make_response(
            jsonify(
                [{"lon": lon, "lat": lat, "temperature": temp} for lat, lon, temp, _ in cur.fetchall()]))
        cur.close()
    return resp


@bp.route("/soilw", methods=['POST'])
def soil_moisture_in_screen():
    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    tid = request_json['tid']
    interval = request_json['interval']

    query = "SELECT * from Polygon_Aggregator_noaa0p25(%s, %s, %s)"
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(north, west, east, south)
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (poly, tid, interval))
        resp = make_response(
            jsonify([{"lon": lon, "lat": lat, "soilw": soilw} for lat, lon, _, soilw in cur.fetchall()]))
        cur.close()
    return resp


@bp.route("/wind")
def wind():
    # TODO: replace source of wind data to db
    resp = make_response(send_from_directory('static/data', 'latest.json'))
    return resp


@bp.route("/rain_fall")
def rainfall():
    # TODO: replace source of rain fall data to db
    resp = make_response(send_from_directory('data', 'rain_fall_sample.csv'))
    return resp


@bp.route("/recent-temp")
def send_temperature_data():
    # This sql gives the second lastest data for temperature within ractangle around US,
    # since the most lastest data is always updating (not completed)
    temperature_fetch = Connection().sql_execute("select t.lat, t.long, t.temperature from recent_temperature t "
                                                 "where t.endtime = (select max(t.endtime) from recent_temperature t"
                                                 " where t.endtime <(select max(t.endtime) from recent_temperature t))")

    temperature_data_celsius = []  # format temp data into a dictionary structure

    for row in temperature_fetch:
        temperature_object = {
            "lat": row[0],
            "long": row[1] % (-360),  # convert longtitude range
            "temp": row[2] - 273.15,  # change temp into celsius
        }

        temperature_data_celsius.append(temperature_object)

    temperature_data_us = points_in_us(temperature_data_celsius)  # restrict data within US boundary.

    resp = make_response(jsonify(temperature_data_us))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # sends temperature data with coordinate within us boundary
    return resp


def points_in_us(pnts: List[Dict[str, float]], accuracy=0.001):
    """
        To filter a list of points dict to a list of them within us boundary
        :param pnts: list of raw points that to be filtered. The format is [{lng: .., lat: .., else: ..}, ...]
        :param accuracy: Allow the path to be made slightly larger or smaller by change the default set of this value.
        :returns: a list of filtered points, in the same format of input pnt dicts
    """
    if not isinstance(pnts, list):
        raise TypeError("Input should be list as : [dict, dict, ...]")

    # TODO: move this bound file to database.
    with open(os.path.join(BOUNDARY_PATH, "USbound.json")) as json_file:
        data = json.load(json_file)
        main_land_poly = mplPath.Path(np.array(data["mainland"][::5]))
        result = []
        for pnt in pnts:
            if main_land_poly.contains_point([pnt['long'] % -360, pnt['lat']], radius=accuracy) \
                    or main_land_poly.contains_point([pnt['long'] % -360, pnt['lat']], radius=-accuracy):
                result.append(pnt)
        return result


@bp.route("/fire", methods=['POST'])
def fire():
    # return a json of all fire name, fire time, and fire geometry inside the bounding box
    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    size = request_json['size']
    start_date = request_json['startDate'][:10]
    end_date = request_json['endDate'][:10]
    size_getters = {0: "get_fire_geom_full", 1: "get_fire_geom_1e4", 2: "get_fire_geom_1e3", 3: "get_fire_geom_1e2",
                    4: "get_center"}
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(east, south, north, west)
    query = f"SELECT * from {size_getters[size]}('{poly}','{start_date}','{end_date}') "

    resp = make_response(jsonify([{"type": "Feature",
                                   "id": "01",
                                   "properties": {"name": name, "agency": agency, "datetime": dt, "density": 520},
                                   "geometry": geom}
                                  for name, agency, dt, geom in Connection.sql_execute(query)]))

    return resp
