import json
import re
import string

import requests
import rootpath
import twitter
from flask import Blueprint, make_response, jsonify, request as flask_request
from router.data_router import fill_series, gen_date_series

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import TWITTER_API_CONFIG_PATH
from utilities.ini_parser import parse

bp = Blueprint('tweet', __name__, url_prefix='/tweet')
api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))


@bp.route("/live-tweet")
def send_live_tweet():
    """
    (unused)(deprecated)
    :return:
    """
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
    """
        This func gives all historical tweets objects with id

        :returns: a list of tweet objects, each with time, lat, long, id
    """
    resp = make_response(
        jsonify([{"create_at": time.isoformat(), "long": lon, "lat": lat, "id": str(id)} for time, lon, lat, _, _, id in
                 Connection().sql_execute(
                     "select r.create_at, l.top_left_long, l.top_left_lat, l.bottom_right_long, l.bottom_right_lat, r.id "
                     "from records r,locations l where r.id=l.id")]))
    return resp


@bp.route("/recent-tweet")
def send_recent_tweet_data():
    """
        This func gives recent tweets objects which must has a image
        here the interval is 10 month

        :returns: a list of tweet objects, each with time, lat, long, text, id
    """
    with Connection() as conn:
        cur = conn.cursor()
        livetweet_query = "select it.create_at, it.top_left_long, it.top_left_lat, it.bottom_right_long, it.bottom_right_lat, it.id, it.text, i.image_url, it.profile_pic, it.user_name " \
                          "from (select r.create_at, l.top_left_long, l.top_left_lat, l.bottom_right_long, l.bottom_right_lat, l.id, r.text, r.profile_pic, r.user_name " \
                          "from records r, locations l where r.id=l.id and r.profile_pic is not null and r.create_at between (SELECT current_timestamp - interval '10 month') and current_timestamp) AS it LEFT JOIN images i on i.id = it.id where i.image_url is not null "
        cur.execute(livetweet_query)
        resp = make_response(
            jsonify(
                [{"create_at": time.isoformat(), "long": long, "lat": lat, "id": id, "text": text, "image": image,
                  "profilePic": profilePic, "user": user} for
                 time, long, lat, _, _, id, text, image, profilePic, user in
                 cur.fetchall()]))
        cur.close()
    return resp


@bp.route('/region-tweet')
def region_tweet():
    """
    tweet count within specific administrative boundary

    @:param tweet_id: integer
    @:param timestamp: ISO string
    @:param days: integer
    :return: [ [date, count], ... ]
    """
    region_id = int(flask_request.args.get('region_id'))
    timestamp_str = flask_request.args.get('timestamp')
    days = int(flask_request.args.get('days', 7))

    # generate date series. values are set to None/null
    date_series = gen_date_series(days, timestamp_str)

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
                SELECT geom from us_counties WHERE county_id={region_id}
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
            fill_series(date_series, cur.fetchall())
        ))
    return resp


@bp.route("/tweet-from-id", methods=['GET'])
def tweet_from_id():
    """
    get detail of specific tweet

    @:param tweet_id: integer
    :return: JSON {"id", "create_at", "text", "user", "profilePic", "image"}
    """
    tweet_id = int(flask_request.args.get('tweet_id'))

    query = '''
    select records.id, create_at, text,user_name,profile_pic,image_url from
    (
        SELECT id, create_at, text,user_name,profile_pic   from records
        WHERE id = %s
    ) as records
    LEFT JOIN
    images
    on records.id = images.id
    LIMIT 1
    '''
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (tweet_id,))
        if cur.rowcount:
            id_, create_at, text, user_name, profile_pic, image_url = cur.fetchone()
            resp = make_response(jsonify({
                'id': str(id_),  # Javascript cannot handle int8, sending as string
                'create_at': create_at,
                'text': text,
                'user': user_name,
                'profilePic': profile_pic,
                'image': image_url
            }))
        else:
            resp = ''

    return resp
