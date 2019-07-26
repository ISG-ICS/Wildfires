import pickle

import rootpath
from flask import Blueprint, make_response, jsonify

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import NLTK_MODEL_PATH
from backend.classifiers.nltktest import NLTKTest

bp = Blueprint('root', __name__, url_prefix='/')
nl: NLTKTest = pickle.load(open(NLTK_MODEL_PATH, 'rb'))


@bp.route("/wildfire-prediction")
def send_wildfire():
    # TODO: update the where clause
    resp = make_response(
        jsonify([{"long": lon, "lat": lat, "nlp": nl.predict(nlp_text), "text": text} for lon, lat, nlp_text, text in
                 Connection().sql_execute(
                     "select l.top_left_long, l.top_left_lat, r.text, r.text from locations l, images i, records r "
                     "where l.id = i.id and r.id = l.id and i.wildfire > 40")]))

    return resp
