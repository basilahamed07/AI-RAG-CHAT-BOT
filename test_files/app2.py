import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from models import db
from test_files.router1 import register_routes
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder for storing uploaded files

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.secret_key = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

# # Flask-Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = "basilahamed46@gmail.com"  # Your email
# app.config['MAIL_PASSWORD'] =  "dhqi eihg aqsn gwiv"
# app.config['MAIL_DEFAULT_SENDER'] = "basilahamed46@gmail.com"

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register the API routes
register_routes(app)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)