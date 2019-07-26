import json
import os
from typing import List, Dict

import matplotlib.path as mplPath
import numpy as np
import rootpath
from flask import Blueprint, make_response, jsonify, send_from_directory, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import BOUNDARY_PATH

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route("/aggregation", methods=['POST'])
def aggregation():
    request_json = flask_request.get_json(force=True)
    lat = float(request_json['lat'])
    lng = float(request_json['lng'])
    radius = float(request_json['radius'])

    query_tweet = 'SELECT * from aggregate_tweet(%s, %s, %s)'
    query2_temp = 'SELECT * from aggregate_temperature(%s, %s, %s)'
    query3_mois = 'SELECT * from aggregate_moisture(%s, %s, %s)'
    with Connection() as conn:
        cur = conn.cursor()

        cur.execute(query_tweet, (lng, lat, radius))  # lng lat
        tweet = cur.fetchone()
        cur.execute(query2_temp, (lat, lng % 360, radius))
        temp = cur.fetchone()
        cur.execute(query3_mois, (lat, lng % 360, radius))
        mois = cur.fetchone()
        resp = make_response(jsonify({'tmp': temp[0] - 273.15, 'soilw': mois[0], 'cnt_tweet': tweet[0]}))

        cur.close()
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
    resp = make_response(send_from_directory('data', 'latest-wind.json'))
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
    temperature_fetch = Connection().sql_execute("select t.lat, t.long, t.temperature from recent_temperature t " \
                                                 "where t.endtime = (select max(t.endtime) from recent_temperature t" \
                                                 " where t.endtime <(select max(t.endtime) from recent_temperature t)) ")

    temperature_data_celsius = []  # format temp data into a dictionary structure

    for row in temperature_fetch:
        temperature_object = {}
        temperature_object["lat"] = row[0]
        temperature_object["long"] = row[1] % (-360)  # convert longtitude range
        temperature_object["temp"] = row[2] - 273.15  # change temp into celsius
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
