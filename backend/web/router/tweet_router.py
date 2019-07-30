import json
import re
import string

import requests
import rootpath
import twitter
from flask import Blueprint, make_response, jsonify, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import TWITTER_API_CONFIG_PATH
from utilities.ini_parser import parse

bp = Blueprint('tweet', __name__, url_prefix='/tweet')
api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))


@bp.route("/live-tweet")
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


@bp.route("/fire-tweet")
def send_fire_tweet_data():
    resp = make_response(
        jsonify([{"create_at": time.isoformat(), "long": lon, "lat": lat} for time, lon, lat, _, _ in
                 Connection().sql_execute(
                     "select r.create_at, l.top_left_long, l.top_left_lat, l.bottom_right_long, l.bottom_right_lat "
                     "from records r,locations l where r.id=l.id")]))
    return resp


@bp.route("/recent-tweet")
def send_recent_tweet_data():
    resp = make_response(
        jsonify([{"create_at": time.isoformat(), "long": long, "lat": lat, "id": id, "text": text} for
                 time, long, lat, _, _, id, text in Connection().sql_execute(
                "select r.create_at,l.top_left_long,l.top_left_lat,l.bottom_right_long,l.bottom_right_lat, l.id, "
                "r.text from records r,locations l where r.id=l.id and r.create_at > NOW() - interval '3 day'")]))

    return resp


@bp.route('/region-tweet')
def region_tweet():
    region_id = int(flask_request.args.get('region_id'))
    timestamp_str = flask_request.args.get('timestamp')
    days = int(flask_request.args.get('days', 7))

    query = '''
    select date(rft.create_at), count(rft."id") from
    (
        SELECT id, create_at from records rec
        where rec.create_at < TIMESTAMP '{timestamp}' -- UTC timezong
        -- returning PDT without timezong label
        and rec.create_at > TIMESTAMP '{timestamp}' - interval '{days} day'
    ) as rft,
    (
        SELECT id from locations loc,
        (
            SELECT geom from us_states WHERE state_id={region_id}
            union
                SELECT geom from us_counties2 WHERE geoid={region_id}
                union
                SELECT geom from us_cities WHERE city_id={region_id}
        ) as region
        where st_contains(region.geom, st_makepoint(loc.top_left_long, loc.top_left_lat))
    ) as gids
    where rft."id"= gids."id"
    GROUP BY date(rft.create_at)
    '''

    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query.format(region_id=region_id, timestamp=timestamp_str, days=days))
        resp = make_response(jsonify(
            [a_row for a_row in cur.fetchall()]
        ))
    return resp
