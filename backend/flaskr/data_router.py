from flask import Blueprint, make_response, jsonify, send_from_directory, request as flask_request

from flaskr.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')


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
    conn = get_db().getconn()
    cur = conn.cursor()
    cur.execute(query, (poly, tid, interval))
    resp = make_response(
        jsonify(
            [{"lng": lon, "lat": lat, "temperature": temperature} for lat, lon, temperature, _ in cur.fetchall()]))
    cur.close()
    get_db().putconn(conn)
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
    conn = get_db().getconn()
    cur = conn.cursor()
    cur.execute(query, (poly, tid, interval))
    resp = make_response(
        jsonify([{"lng": lon, "lat": lat, "soilw": soilw} for lat, lon, _, soilw in cur.fetchall()]))
    cur.close()
    get_db().putconn(conn)
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
