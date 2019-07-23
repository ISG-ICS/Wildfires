import pickle
import random

import rootpath

rootpath.append()

from backend.data_preparation.connection import Connection
from backend.classifiers.nltktest import NLTKTest

import twitter
import json
import requests
import re
import string
import matplotlib.path as mplPath
import numpy as np
from typing import List, Dict
import os
from utilities.ini_parser import parse

from flask import Flask, send_from_directory, make_response, jsonify, request as flask_request
from flask_cors import CORS

from paths import NLTK_MODEL_PATH, BOUNDARY_PATH, TWITTER_API_CONFIG_PATH

app = Flask(__name__, static_url_path='')
CORS(app)
app.config.from_pyfile('server_config.py', silent=True)

# load abbreviation of states
with open('us_states_abbr.json', 'r') as f:
    us_states_abbr: Dict = json.load(f)

nl: NLTKTest = pickle.load(open(NLTK_MODEL_PATH, 'rb'))
api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))


@app.route("/search")
def send_search_data():
    keyword = flask_request.args.get('keyword')

    # load abbreviation
    if keyword in us_states_abbr:
        keyword = us_states_abbr[keyword]

    search_state = "SELECT state_name, st_asgeojson(t.geom) from us_states t where state_name=%s"
    search_city = "SELECT city_name, st_asgeojson(t.geom) from us_cities t where city_name=%s limit 1"
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(search_state, (keyword,))
        results = [json.loads(geom) for name, geom in cur.fetchall()]
        if not results:
            cur.execute(search_city, (keyword,))
            results = [json.loads(geom) for name, geom in cur.fetchall()]
        resp = make_response(jsonify(results))
        cur.close()
    return resp


@app.route("/boundaries", methods=['POST', 'GET'])
def send_boundaries_data():
    request_json = flask_request.get_json(force=True)
    states = request_json['states']
    cities = request_json['cities']
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']

    select_states = "SELECT * from select_states_intersects(%s)"
    select_cities = "SELECT * from select_cities_intersects(%s)"
    poly = 'polygon(({1} {0}, {2} {0}, {2} {3}, {1} {3}, {1} {0}))'.format(north, west, east, south)  # lon lat
    with Connection() as conn:
        cur = conn.cursor()

        if states:
            cur.execute(select_states, (poly,))
        elif cities:
            cur.execute(select_cities, (poly,))
        resp = make_response(
            jsonify(
                [{"type": "Feature", "properties": {"name": "Alabama", "density": random.random() * 1200},
                  "geometry": json.loads(geom)}
                 for _, geom in cur.fetchall()]))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        cur.close()
    return resp


@app.route("/temp", methods=['POST', 'GET'])
def send_temp_data():
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
                [{"lng": lon, "lat": lat, "temperature": temperature} for lat, lon, temperature, _ in cur.fetchall()]))
        cur.close()
    return resp


@app.route("/soilw", methods=['POST', 'GET'])
def send_soil_data():
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
            jsonify([{"lng": lon, "lat": lat, "soilw": soilw} for lat, lon, _, soilw in cur.fetchall()]))
        cur.close()
    return resp


@app.route("/wind")
def send_wind_data():
    # TODO: replace source of wind data to db
    resp = make_response(send_from_directory('data', 'latest-wind.json'))
    return resp


@app.route("/rain_fall")
def send_realtime_data():
    # TODO: replace source of rain fall data to db
    resp = make_response(send_from_directory('data', 'rain_fall_sample.csv'))
    return resp


@app.route("/live_tweet")
def send_live_tweet():
    # TODO: replace source of live tweets to db
    # Simulate request from a mac browser
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.121 Safari/537.36 '
    }

    query_words = 'fire'  # for now let's use fire for testing

    resp = requests.get(
        f'https://twitter.com/i/search/timeline?f=tweets&vertical=news&q={query_words}%20near%3A\"United%20States'
        f'\"%20within%3A8000mi&l=en&src=typd', headers=headers)

    # Clear all punctuation from raw response body
    tr = str.maketrans("", "", string.punctuation)
    content = str(resp.content)
    content = content.translate(tr)

    id_set = set()
    return_dict = list()
    for id in re.findall("dataitemid(\d+)", content):
        obj = json.loads(str(api.GetStatus(id)))
        if "place" in obj and obj["id"] not in id_set:
            left = obj["place"]['bounding_box']['coordinates'][0][0]
            right = obj["place"]['bounding_box']['coordinates'][0][2]
            center = [(x + y) / 2.0 for x, y in zip(left, right)]
            id_set.add(obj["id"])
            return_dict.append({"lat": center[1], "long": center[0], "id": id})
    resp = make_response(jsonify(return_dict))
    return resp


@app.route("/tweets")
def send_tweets_data():
    resp = make_response(
        jsonify([{"create_at": time.isoformat(), "long": lon, "lat": lat} for time, lon, lat, _, _ in
                 Connection().sql_execute(
                     "select r.create_at, l.top_left_long, l.top_left_lat, l.bottom_right_long, l.bottom_right_lat "
                     "from records r,locations l where r.id=l.id")]))
    return resp


@app.route("/wildfire_prediction")
def send_wildfire():
    # TODO: update the where clause
    resp = make_response(
        jsonify([{"long": lon, "lat": lat, "nlp": nl.predict(text)} for lon, lat, text in Connection().sql_execute(
            "select l.top_left_long, l.top_left_lat, r.text from locations l, images i, records r where l.id = i.id "
            "and r.id = l.id and i.wildfire > 40")]))

    return resp


@app.route("/recent-temp")
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


if __name__ == "__main__":
    app.run(threaded=True)
