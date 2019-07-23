import json
from flaskr.db import get_db
from flask import Blueprint, make_response, jsonify, request as flask_request

bp = Blueprint('search', __name__, url_prefix='/search')

# load abbreviation of states
with open('us_states_abbr.json', 'r') as f:
    us_states_abbr: dict = json.load(f)


@bp.route('', methods=('GET', 'POST'))
def search():
    keyword = flask_request.args.get('keyword')

    # load abbreviation
    if keyword in us_states_abbr:
        keyword = us_states_abbr[keyword]

    search_state = "SELECT state_name, st_asgeojson(t.geom) from us_states t where state_name=%s"
    search_city = "SELECT city_name, st_asgeojson(t.geom) from us_cities t where city_name=%s limit 1"

    conn = get_db()
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
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']

    select_states = "SELECT * from select_states_intersects(%s)"
    select_cities = "SELECT * from select_cities_intersects(%s)"
    poly = 'polygon(({1} {0}, {2} {0}, {2} {3}, {1} {3}, {1} {0}))'.format(north, west, east, south)  # lon lat
    conn = get_db()
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
