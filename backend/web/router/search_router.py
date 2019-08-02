import json
import random

import rootpath
from flask import Blueprint, make_response, jsonify, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('', methods=['GET'])
def search_administrative_boundaries():
    keyword = flask_request.args.get('keyword')

    # if kw is an id, get geometry directly
    try:
        region_id = int(keyword)
    except ValueError:
        pass
    else:
        # is a region_id
        query = f'''
        SELECT st_asgeojson(t.geom) as geojson from us_states t where state_id = {region_id}
        union
        SELECT st_asgeojson(t.geom) as geojson from us_counties2 t where geoid = {region_id}
        union
        SELECT st_asgeojson(t.geom) as geojson from us_cities t where city_id = {region_id}
        '''

        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            resp = make_response(jsonify(
                [json.loads(geom) for geom, in cur.fetchall()]
            ))
            cur.close()
        return resp

    # load abbreviation
    keyword = us_states_abbr.get(keyword, keyword)

    search_state = "SELECT st_asgeojson(t.geom) from us_states t where state_name=%s"

    # TODO: implement autocomplete in keyword selection, replace LIMIT 1
    search_city = "SELECT st_asgeojson(t.geom) from us_cities t where city_name=%s limit 1"

    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(search_state, (keyword,))
        results = [json.loads(geom) for geom, in cur.fetchall()]
        if not results:
            cur.execute(search_city, (keyword,))
            results = [json.loads(geom) for geom, in cur.fetchall()]
        resp = make_response(jsonify(results))
        cur.close()
    return resp


@bp.route("/boundaries", methods=('POST',))
def send_boundaries_data():
    request_json = flask_request.get_json(force=True)
    states = request_json['states']
    cities = request_json['cities']
    counties = request_json['counties']
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']

    select_states = "SELECT * from boundaries_states(%s)"
    select_counties = "SELECT * from boundaries_counties(%s)"
    select_cities = "SELECT * from boundaries_cities(%s)"
    poly = 'polygon(({1} {0}, {2} {0}, {2} {3}, {1} {3}, {1} {0}))'.format(north, west, east, south)  # lon lat +-180

    with Connection() as conn:
        cur = conn.cursor()
        result_list = list()

        if states:
            result_list.extend(_get_geometry(cur, select_states, poly))
        if counties:
            result_list.extend(_get_geometry(cur, select_counties, poly))
        if cities:
            result_list.extend(_get_geometry(cur, select_cities, poly))

    resp = make_response(jsonify(result_list))
    cur.close()
    return resp


def _get_geometry(cur, sql, poly) -> list:
    # FIXME: density is random...

    cur.execute(sql, (poly,))
    return [{"type": "Feature", "id": _id,
             "properties": {"name": name, "density": random.random() * 1200},
             "geometry": json.loads(geojson)} for _id, name, geojson, _ in cur.fetchall()]


# abbreviation of states
us_states_abbr = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
                  "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
                  "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
                  "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
                  "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
                  "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
                  "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
                  "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
                  "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
                  "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
