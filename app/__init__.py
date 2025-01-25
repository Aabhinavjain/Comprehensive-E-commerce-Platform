# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        # Default to DevelopmentConfig if no config_class is provided
        config_class = os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig')
    
    # Load configuration from the provided config class
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"

    # Import models after initializing db to avoid circular imports
    from .models import User, Product, Order, OrderItem, CartItem

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .routes import main
    from .auth import auth_bp
    from .admin import admin_bp
    from .cart import cart_bp  # Ensure you have a cart blueprint

    app.register_blueprint(main)      # Homepage/Product listing
    app.register_blueprint(auth_bp)   # Login/Register
    app.register_blueprint(admin_bp)  # Admin functionalities
    app.register_blueprint(cart_bp)   # Cart functionalities

    return app
