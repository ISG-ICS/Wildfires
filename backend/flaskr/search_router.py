import json
import random
import os
import rootpath

from flask import Blueprint, make_response, jsonify, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection

bp = Blueprint('search', __name__, url_prefix='/search')

# load abbreviation of states
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'us_states_abbr.json'), 'r') as f:
    us_states_abbr: dict = json.load(f)


@bp.route('', methods=('GET', 'POST'))
def search():
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


@bp.route("/boundaries", methods=['POST', 'GET'])
def send_boundaries_data():
    request_json = flask_request.get_json(force=True)
    states = request_json['states']
    cities = request_json['cities']
    counties = request_json['counties']
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']

    select_states = "SELECT * from select_states_intersects(%s)"
    select_counties = "SELECT * from select_counties_intersects(%s)"
    select_cities = "SELECT * from select_cities_intersects(%s)"
    poly = 'polygon(({1} {0}, {2} {0}, {2} {3}, {1} {3}, {1} {0}))'.format(north, west, east, south)  # lon lat

    with Connection() as conn:
        cur = conn.cursor()
        result_list = list()
        if states:
            cur.execute(select_states, (poly,))
            result_list.extend([{"type": "Feature",
                                 "properties": {"name": name, "density": random.random() * 1200},
                                 "geometry": json.loads(geom)} for name, geom in cur.fetchall()])
        if counties:
            cur.execute(select_counties, (poly,))
            result_list.extend([{"type": "Feature",
                                 "properties": {"name": name, "density": random.random() * 1200},
                                 "geometry": json.loads(geom)} for name, geom in cur.fetchall()])
        if cities:
            cur.execute(select_cities, (poly,))
            result_list.extend([{"type": "Feature",
                                 "properties": {"name": name, "density": random.random() * 1200},
                                 "geometry": json.loads(geom)} for name, geom in cur.fetchall()])

    resp = make_response(jsonify(result_list))
    cur.close()
    return resp
