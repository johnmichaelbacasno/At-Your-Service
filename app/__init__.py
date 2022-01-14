from flask import Flask

from .views.main import main
from .views.miscellaneous import miscellaneous

from extensions import *

def create_app():
    # Initialize app
    app = Flask(__name__)
    
    # Initialize config
    app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    db.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    session.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    with app.app_context():
        # Register blueprints
        app.register_blueprint(main)
        app.register_blueprint(miscellaneous)
    
    return app