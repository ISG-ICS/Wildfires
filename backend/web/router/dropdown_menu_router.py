import rootpath

rootpath.append()
from flask import Blueprint, make_response, jsonify, request as flask_request
from backend.connection import Connection

bp = Blueprint('dropdownMenu', __name__, url_prefix='/dropdownMenu')


@bp.route('')
def drop_box():
    """
    auto-completion relies on this API.
    frontend send user types through userInput,
    this API perform DB query through stored procedure (autocomplete.sql)

    return a list/array: [ (city, county, state, id), ... ]
    :return:
    """
    user_input = flask_request.args.get('userInput')
    # request_json = flask_request.get_json(force=True)
    # user_input = request_json['userInput']
    name_list_query = f"select * from fuzzy_search('{user_input + '%'}')"

    return make_response(jsonify(list(Connection.sql_execute(name_list_query))))
