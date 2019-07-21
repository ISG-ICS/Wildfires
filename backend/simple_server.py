import json
import pickle
import re
import string
from typing import Dict

import requests
import rootpath
import twitter

rootpath.append()
from backend.data_preparation.connection import Connection
from backend.classifiers.nltktest import NLTKTest
from utilities.ini_parser import parse

from flask import Flask, send_from_directory, make_response, jsonify, request as flask_request

from paths import NLTK_MODEL_PATH, TWITTER_API_CONFIG_PATH

app = Flask(__name__, static_url_path='')
app.config.from_pyfile('server_config.py', silent=True)

# load states
with open('us_states_dict.json', 'r') as f:
    us_states: Dict = json.load(f)

# load abbreviation of states
with open('us_states_abbr.json', 'r') as f:
    us_states_abbr: Dict = json.load(f)

nl: NLTKTest = pickle.load(open(NLTK_MODEL_PATH, 'rb'))
api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))


@app.route("/search")
def send_search_data():
    keyword = flask_request.args.get('keyword')

    # currently we can search states from in-memory-dict
    search_result = None
    if keyword in us_states:
        search_result = us_states[keyword]
    elif keyword in us_states_abbr:
        search_result = us_states[us_states_abbr[keyword]]
    resp = make_response(jsonify(search_result.get('geometry') if search_result else None))
    resp.headers['Access-Control-Allow-Origin'] = '*'
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
            jsonify([{"lng": lon, "lat": lat, "temperature": value} for lat, lon, value in cur.fetchall()]))
        resp.headers['Access-Control-Allow-Origin'] = '*'
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
    poly = 'polygon(({0} {1}, {0} {2}, {3} {2}, {3} {1}, {0} {1}))'.format(north, west, east, south)
    with Connection() as conn:
        cur = conn.cursor()

        if states:
            cur.execute(select_states, (poly,))
        elif cities:
            cur.execute(select_cities, (poly,))
        resp = make_response(
            jsonify([{"geometry": json.loads(geom)} for _, geom in cur.fetchall()]))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        cur.close()
    return resp


@app.route("/wind")
def send_wind_data():
    # TODO: replace source of wind data to db
    resp = make_response(send_from_directory('data', 'latest-wind.json'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/rain_fall")
def send_realtime_data():
    # TODO: replace source of rain fall data to db
    resp = make_response(send_from_directory('data', 'rain_fall_sample.csv'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
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
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/tweets")
def send_tweets_data():
    resp = make_response(
        jsonify([{"create_at": time.isoformat(), "long": lon, "lat": lat} for time, lon, lat, _, _ in
                 Connection().sql_execute(
                     "select r.create_at, l.top_left_long, l.top_left_lat, l.bottom_right_long, l.bottom_right_lat "
                     "from records r,locations l where r.id=l.id")]))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/wildfire_prediction")
def send_wildfire():
    # TODO: update the where clause
    resp = make_response(
        jsonify([{"long": lon, "lat": lat, "nlp": nl.predict(text)} for lon, lat, text in Connection().sql_execute(
            "select l.top_left_long, l.top_left_lat, r.text from locations l, images i, records r where l.id = i.id "
            "and r.id = l.id and i.wildfire > 40")]))
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


if __name__ == "__main__":
    app.run()
