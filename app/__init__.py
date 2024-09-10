from flask import Flask
import os
from .models import db
from .routes import main
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    
    
    # Configuration for SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Initialize the database with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app
