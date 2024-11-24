from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    positions = db.Column(db.String(10), nullable=False, default='normal')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'positions': self.positions,
        }

class File(db.Model):
    __tablename__ = 'file_details'  # Table name is fine, though it's lowercase as per convention
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    file_type = db.Column(db.String(256), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  # Added field to store file content
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp for file creation

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'created_at': self.created_at,
        }

class Product(db.Model):
    __tablename__ = 'AI_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    questions = db.Column(db.String(255), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file_details.id'), nullable=False)  # Foreign key to File
    file_details = db.relationship('File', backref=db.backref('AI_info', lazy=True))  # Corrected relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('AI_info', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'questions': self.questions,
            'file_id': self.file_id,  # Corrected to file_id, referencing the file
            'user_id': self.user_id,  # Correct field referencing the User
        }
    