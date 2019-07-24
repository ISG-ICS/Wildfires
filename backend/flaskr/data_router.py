import rootpath

from flask import Blueprint, make_response, jsonify, send_from_directory, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route("/aggregation", methods=['POST', 'GET'])
def aggregation():
    request_json = flask_request.get_json(force=True)
    lat = float(request_json['lat'])
    lon = float(request_json['lon'])
    radius = float(request_json['radius'])

    query_tweet = 'SELECT * from aggregate_tweet(%s, %s, %s)'
    query2_temp = 'SELECT * from aggregate_temperature(%s, %s, %s)'
    query3_mois = 'SELECT * from aggregate_moisture(%s, %s, %s)'
    with Connection() as conn:
        cur = conn.cursor()

        cur.execute(query_tweet, (lon, lat, radius))
        tweet = cur.fetchone()
        cur.execute(query2_temp, (lon, lat, radius))
        temp = cur.fetchone()
        cur.execute(query3_mois, (lon, lat, radius))
        mois = cur.fetchone()
        resp = make_response(jsonify({'tmp': temp[0], 'soilw': mois[0], 'cnt_tweet': tweet[0]}))

        cur.close()
    return resp


@bp.route("/temp", methods=['POST', 'GET'])
def temperature():
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
                [{"lng": lon, "lat": lat, "temperature": temp} for lat, lon, temp, _ in cur.fetchall()]))
        cur.close()
    return resp


@bp.route("/soilw", methods=['POST', 'GET'])
def soil():
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
