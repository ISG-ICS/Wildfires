from flask import Flask
from flask_cors import CORS
import search_router
import data_router


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(search_router.bp)
    app.register_blueprint(data_router.bp)

    return app


if __name__ == '__main__':
    server_app = create_app()
    server_app.run(debug=True)
