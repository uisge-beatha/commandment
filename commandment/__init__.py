"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from flask import Flask, render_template
from flask_jwt import JWT

from .omdm_app import omdm_app
from .configuration import configuration_app
from .mdm_app import mdm_app
from .mdmcert import admin_mdmcert_app
from .api import api_app
from .api_push import api_push_app
from .api_flat import flat_api
from .enroll import enroll_app
from .ota import ota_app
from .sso.oauth import oauth_app
from .sso.saml import saml_app
from .models import db
from .auth import authenticate, identity


def create_app() -> Flask:
    """Create the Flask Application

    Returns:
        Instance of the flask application
    """
    app = Flask(__name__)
    app.config.from_object('commandment.default_settings')
    app.config.from_envvar('COMMANDMENT_SETTINGS', True)

    db.init_app(app)
    db.create_all(app=app)

    jwt = JWT(app, authenticate, identity)

    app.register_blueprint(enroll_app, url_prefix='/enroll')
    app.register_blueprint(mdm_app)
    app.register_blueprint(admin_mdmcert_app, url_prefix='/admin/mdmcert')
    app.register_blueprint(configuration_app, url_prefix='/api/v1/configuration')
    app.register_blueprint(api_app, url_prefix='/api')
    app.register_blueprint(api_push_app, url_prefix='/api')
    app.register_blueprint(flat_api, url_prefix='/api')
    app.register_blueprint(ota_app, url_prefix='/ota')
    app.register_blueprint(oauth_app, url_prefix='/oauth')
    app.register_blueprint(saml_app, url_prefix='/saml')
    app.register_blueprint(omdm_app, url_prefix='/omdm')

    # SPA Entry Point
    @app.route('/')
    def index():
        """Main entry point for the administrator web application."""
        return render_template('index.html')

    # SPA history fallback handler
    @app.errorhandler(404)
    def send_index(path: str):
        """Fallback route for HTML5 History."""
        return render_template('index.html')

    return app

