import rootpath
from flask import Flask
from flask_cors import CORS

rootpath.append()
import router.data_router
import router.dropdown_menu_router
import router.search_router
import router.tweet_router
import router.root_router
import logging
from flask_compress import Compress

logging.basicConfig(level=logging.DEBUG)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='', static_folder='static')
    # Enable CORS, cross-site-access-control
    Compress().init_app(app)
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
    app.register_blueprint(router.dropdown_menu_router.bp)

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    from waitress import serve

    server_app = create_app()

    parser = ArgumentParser()
    parser.add_argument("--deploy", help="deploy server in production mode",
                        action="store_true")
    args = parser.parse_args()
    if args.deploy:
        serve(server_app, host='0.0.0.0', port=2333)
    else:
        server_app.run(port=5000, debug=True)
