import rootpath
from flask import Flask
from flask_cors import CORS

import router.data_router
import router.dropDownMenu_router
import router.search_router
import router.tweet_router

rootpath.append()
# TODO: change model loading
from backend.classifiers.nltktest import NLTKTest  # must import NLTKTest before root_router

nl: NLTKTest  # to avoid NLTKTest importation being optimized by IDE
import router.root_router


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static', static_folder='static')
    # Enable CORS, cross-site-access-control
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # TODO: implement a config file (ini / json)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # register routers
    app.register_blueprint(router.search_router.bp)
    app.register_blueprint(router.data_router.bp)
    app.register_blueprint(router.tweet_router.bp)
    app.register_blueprint(router.root_router.bp)
    app.register_blueprint(router.dropDownMenu_router.bp)

    return app


if __name__ == '__main__':
    server_app = create_app()
    server_app.run(debug=True)
