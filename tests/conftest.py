# tests/conftest.py

import pytest
from app import create_app, db
from app.models import User, Product
from app.config import TestingConfig
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@pytest.fixture(scope='module')
def app():
    """
    Create and configure a new app instance for each test module.
    """
    # Configure the app for testing
    app = create_app(TestingConfig)
    
    # Create the database and the database table
    with app.app_context():
        db.create_all()
        
        # Create a test user with hashed password
        hashed_password = bcrypt.generate_password_hash('secret123').decode('utf-8')
        user = User(username='testuser', email='test@example.com', password=hashed_password)
        db.session.add(user)
        
        # Create a test product
        product = Product(name='Test Product', description='Test Description', price=19.99, image='test.jpg')
        db.session.add(product)
        
        db.session.commit()
        
        yield app  # this is where the testing happens!
        
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """
    A test runner for the app's Click commands.
    """
    return app.test_cli_runner()
