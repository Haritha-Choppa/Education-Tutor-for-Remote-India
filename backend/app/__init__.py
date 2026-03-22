from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "..", "instance", "tutoring.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-this-secret')

    # Password reset / mail configuration
    app.config['PASSWORD_RESET_TOKEN_EXPIRY_MINUTES'] = int(os.environ.get('PASSWORD_RESET_TOKEN_EXPIRY_MINUTES', '30'))
    app.config['FRONTEND_URL'] = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', '')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_FROM'] = os.environ.get('MAIL_FROM', app.config['MAIL_USERNAME'])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Create instance folder
    instance_path = os.path.join(basedir, '..')
    if not os.path.exists(os.path.join(instance_path, 'instance')):
        os.makedirs(os.path.join(instance_path, 'instance'))
    
    # Register blueprints
    from app.routes import users, lessons, quizzes, messages, progress
    app.register_blueprint(users.bp)
    app.register_blueprint(lessons.bp)
    app.register_blueprint(quizzes.bp)
    app.register_blueprint(messages.bp)
    app.register_blueprint(progress.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
