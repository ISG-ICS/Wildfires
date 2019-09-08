import pickle
import time

import rootpath
from flask import Blueprint, make_response, jsonify, request as flask_request

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import NLTK_MODEL_PATH
from backend.classifiers.nltktest import NLTKTest

bp = Blueprint('root', __name__, url_prefix='/')
nl: NLTKTest = pickle.load(open(NLTK_MODEL_PATH, 'rb'))


@bp.route("/wildfire-prediction", methods=['POST'])
def send_wildfire():
    """
    provide predicted wildfires
    :return:
    """
    # TODO: update the where clause
    request_json = flask_request.get_json(force=True)
    north = request_json['northEast']['lat']
    east = request_json['northEast']['lon']
    south = request_json['southWest']['lat']
    west = request_json['southWest']['lon']
    start = request_json['startDate']
    end = request_json['endDate']
    start = time.mktime(time.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ"))
    end = time.mktime(time.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ"))

    resp = make_response(
        jsonify([{"long": lon, "lat": lat, "nlp": nl.predict(nlp_text), "text": text} for lon, lat, nlp_text, text in
                 Connection().sql_execute(
                     f"select l.top_left_long, l.top_left_lat, r.text, r.text from locations l, images i, records r "
                     f"where l.id = i.id and r.id = l.id and i.wildfire_prob>0.9 and l.top_left_long>{west} and l.top_left_lat<{north} "
                     f"and l.bottom_right_long<{east} and l.bottom_right_lat>{south} and extract(epoch from r.create_at) >{start} and extract(epoch from r.create_at) <{end}")]))
    return resp
