from flask import Blueprint, make_response, jsonify, request as flask_request

from utilities.connection import Connection

bp = Blueprint('dropdownMenu', __name__, url_prefix='/dropdownMenu')


@bp.route('', methods=['GET'])
def dropBox():
    userInput = flask_request.args.get('userInput')
    # request_json = flask_request.get_json(force=True)
    # userInput = request_json['userInput']
    name_list = "select * from fuzzy_search(%s);"

    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(name_list, (userInput + "%",))
        resp = make_response(jsonify(cur.fetchall()))
        cur.close()
    return resp
