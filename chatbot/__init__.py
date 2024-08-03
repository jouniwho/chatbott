import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

db = SQLAlchemy()

def create_app(test_config=None):
    """
    Create app based on config or test_config
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    #add API documentation, url: /apidocs/
    app.config["SWAGGER"] = {
        "title": "chatbot",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/chatbot.yml")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as error:
        print(error)

    db.init_app(app)

    from . import models
    from . import api
    from chatbot.utils import chatConverter
    app.url_map.converters["chat"] = chatConverter
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.fill_db_command)
    app.register_blueprint(api.api_bp)

    return app
