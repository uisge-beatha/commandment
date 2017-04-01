"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from flask import Flask, render_template

from .mdm import mdm_app
from .admin import admin_app
from .mdmcert import admin_mdmcert_app
from .api import api_app
from .api_push import api_push_app
from .models import db


def create_app(config_filename: str) -> Flask:
    """Create the Flask Application

    Args:
        config_filename: Path to the configuration file to load (settings.cfg)
    Returns:
        Instance of the flask application
    """
    app = Flask(__name__)
    app.config.from_object('commandment.default_settings')
    app.config.from_pyfile(config_filename)
    db.init_app(app)

    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_app)
    app.register_blueprint(admin_mdmcert_app, url_prefix='/admin/mdmcert')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(api_push_app, url_prefix='/api')

    # SPA history fallback handler
    @app.errorhandler(404)
    def send_index(path: str):
        return render_template('index.html')

    return app

UPLOADCERT_SUPPORTED_MIMETYPES = [
    'application/x-pem-file',
    'application/x-x509-user-cert',
    'application/x-x509-ca-cert',
    'application/x-pkcs12'
]
