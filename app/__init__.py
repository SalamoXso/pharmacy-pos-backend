from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load config

    print("Database URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))  # Debugging

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # ✅ Initialize JWT
    CORS(app)

    # Register blueprints (routes)
    from app.routes import main_bp
    from app.routes.auth import auth_bp  # ✅ Ensure auth routes are registered

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)  # ✅ Register authentication routes

    return app
