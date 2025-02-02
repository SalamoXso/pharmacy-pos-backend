from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config  # Ensure this import is correct

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load config

    print("Database URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))  # Debugging

    db.init_app(app)  # This line is failing, meaning config isn't loading
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints (routes)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
