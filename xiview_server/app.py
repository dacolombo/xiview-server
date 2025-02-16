import json
import urllib

import psycopg2
from flask import Flask, render_template
from flask_cors import CORS
# import logging.config

# logging.config.fileConfig('logging.ini')
# logger = logging.getLogger(__name__)

def create_app():
    """
    Create the flask app.

    :return: flask app
    """
    app = Flask(__name__, static_url_path="",
                static_folder='../static', template_folder='../templates')

    # Load flask config, TODO: app.env is deprecated
    if app.env == 'development':
        app.config.from_object('xiview_server.config.DevelopmentConfig')
    else:
        app.config.from_object('xiview_server.config.ProductionConfig')
        try:
            app.config.from_envvar('XI2XIVIEWLOADER_SETTINGS')
        except (FileNotFoundError, RuntimeError):
            ...

    # add CORS header
    CORS(app)

    from xi2annotator import bp as xi2_bp
    app.register_blueprint(xi2_bp)

    @app.route('/', methods=['GET'])
    def index():
        # fetch datasets from http://127.0.0.1:8081/pride/archive/xiview/ws/data/get_datasets
        with urllib.request.urlopen("http://127.0.0.1:8081/pride/archive/xiview/ws/data/get_datasets") as url:
            ds_rows = json.load(url)
            return render_template("datasets.html", datasets=ds_rows)

    @app.route('/network.html', methods=['GET'])
    def network():
        return app.send_static_file('network.html')

    return app
