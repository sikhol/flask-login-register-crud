from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config
db = SQLAlchemy()
def create_app(config_class=Config):
    app = Flask(__name__,template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)
    Migrate(app, db, compare_type=True)
    from controllers.main import index
    app.register_blueprint(index)

    return app
