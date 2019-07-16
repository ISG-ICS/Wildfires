import pickle

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
from typing import List,Dict



import pygrib

from flask import Flask, send_from_directory, make_response, jsonify

from paths import NLTK_MODEL_PATH

app = Flask(__name__, static_url_path='')


nl: NLTKTest = pickle.load(open(NLTK_MODEL_PATH, 'rb'))
api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")

tweet_query = "select r.create_at, l.top_left_long, l.top_left_lat, l.bottom_right_long, l.bottom_right_lat " \
              "from records r,locations l where r.id=l.id"


@app.route("/temp")
def send_temp_data():
    query = "select * from recent_temperature "
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        resp = make_response(
            jsonify([{"lng": long, "lat": lat, "temperature": value} for lat, long, value, _ in cur.fetchall()]))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        cur.close()
    return resp


@app.route("/wind")
def send_wind_data():
    grbs = pygrib.open('gfs.t12z.pgrb2.0p25.anl')
    grbs.seek(0)
    result_list = []
    result = {}
    result['header'] = {}
    result['data'] = np.array([])
    for g in grbs:
        # OPTIMIZE: duplication with grib_converter.py
        for row in g['values']:
            result['data'] = np.concatenate((result['data'], row), axis=0)

        result['header'] = {
            'parameterCategory': g["parameterCategory"],
            'parameterNumber': g['parameterNumber'],
            'numberPoints': len(result['data']),
            'nx': g['Ni'],
            'ny': g['Nj'],
            'lo1': g['longitudeOfFirstGridPointInDegrees'],
            'lo2': g['longitudeOfLastGridPointInDegrees'],
            'la1': g['latitudeOfFirstGridPointInDegrees'],
            'la2': g['latitudeOfLastGridPointInDegrees'],
            'dx': g['iDirectionIncrementInDegrees'],
            'dy': g['jDirectionIncrementInDegrees'],
        }
        result['data'] = result['data'].tolist()
        result_list.append(result)
        result = {}
        result['header'] = {}
        result['data'] = []
        resp = make_response(jsonify(result_list))
    # resp = make_response(send_from_directory('','2019070312.json'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/rain_fall")
def send_realtime_data():
    resp = make_response(send_from_directory('data', 'rain_fall_sample.csv'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/live_tweet")
def send_live_tweet():
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
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(tweet_query)

        resp = make_response(
            jsonify(
                [{"create_at": time.isoformat(), "long": long, "lat": lat} for time, long, lat, _, _ in
                     cur.fetchall()]))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        cur.close()
    return resp


@app.route("/wildfire_prediction")
def send_wildfire():
    query = "select l.top_left_long, l.top_left_lat, r.text from locations l, images i, records r " \
            "where l.id = i.id and r.id = l.id and i.wildfire > 40;"
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query)

        resp = make_response(
            jsonify([{"long": long, "lat": lat, "nlp": nl.predict(text)} for long, lat, text in cur.fetchall()]))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        cur.close()
    return resp


@app.route("/recenttemp")
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

        returns a list of filtered points dictionary within the US boundary.

        :param pnts: list of raw points that going to be filtered, in the format [{lng: .., lat: .., else: ..}, ...]
        :param accuracy: accuracy theta for ???? <I don't know what the accuracy is used for?>

        :returns: a list of filtered points, in the same format of input pnt
    """
    if not isinstance(pnts, list):
        raise TypeError("Input should be list as : [dict, dict, ...]")

    with open("USbound.json") as json_file:
        data = json.load(json_file)
        main_land_poly = mplPath.Path(np.array(data["mainland"][::5]))
        result = []
        for pnt in pnts:
            if main_land_poly.contains_point([pnt['long'] % -360, pnt['lat']], radius=accuracy) \
                    or main_land_poly.contains_point([pnt['long'] % -360, pnt['lat']], radius=-accuracy):
                result.append(pnt)
        return result


if __name__ == "__main__":
    app.run()
