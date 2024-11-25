from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager,jwt_manager,get_jwt_identity
from dotenv import load_dotenv
import os
from models import db
from router import register_routes
load_dotenv()



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost/AI-CHAT-BOT'  # SQLite database for simplicity
app.config['csv_file'] = 'uploads/csv'  # Folder where uploaded files will be stored
app.config['ALLOWED_EXTENSIONS'] = {"csv"}  # Allowed file extensions
app.secret_key = os.getenv("SECRET_KEY")  # Required for forms (CSRF protection)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

#configure and initilize the apps for below code

CORS(app)
db.init_app(app)
migrate = Migrate(app,db)
jwd = JWTManager(app)

# @register the api routers

register_routes(app)

#create the database 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)