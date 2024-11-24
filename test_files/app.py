import fitz  # PyMuPDF
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import time
from preprocessing import load_documets,text_splitter # Ensure this is your preprocessing module that works

# Initialize the Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Database%40123@localhost/test_db'  # Database URI
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder where uploaded files will be stored
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions
app.secret_key = 'your_secret_key'  # Required for forms (CSRF protection)

db = SQLAlchemy(app)

# File model (already provided in the question)


class index_data(db.Model):
    __tablename__ = 'index_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index_file_path = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'index_file_path': self.index_file_path,
            'created_at': self.created_at,
        }


class File(db.Model):
    __tablename__ = 'file_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    file_type = db.Column(db.String(256), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    index_id = db.Column(db.Integer, db.ForeignKey('index_data.id'), nullable=True)
    users = db.relationship('index_data', backref=db.backref('index_data', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'created_at': self.created_at,
        }
    


# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload a file
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file_type = file.mimetype
            # file_data = file.read()  # Get the file content

            # Check if the file is empty after reading
            # if len(file_data) == 0:
            #     print*()
            #     return 'Uploaded file is empty. Please upload a valid file.'

            # Save the file to the server
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(upload_path)  # Save the file to the uploads folder
            
            # Check if the file is actually saved and not empty
            if os.path.getsize(upload_path) == 0:
                return 'Uploaded file is empty. Please upload a valid file.'
            
            print(f"File saved successfully to {upload_path}")

            # Save file metadata to the database
            new_file = File(filename=filename, file_type=file_type, file_data=file.read())
            db.session.add(new_file)
            db.session.commit()

            # AI processing (e.g., extracting text)
            time.sleep(5)  # Simulating AI processing delay
            
            # Check if file is a PDF and process
            if file_type == 'application/pdf':
                pages = load_documets(upload_path)
                print(f"Extracted pages: {pages}")
            print(pages)

            chunked = text_splitter(pages)
            print(len(chunked))
            # Redirect or return a success message
            # return pages
            return redirect(url_for('uploaded_files'))
            # r
    return render_template('upload.html')

# Function to extract text from a PDF file using the file path
def extract_pdf_text(file_path):
    try:
        # Open the saved PDF file from the file path using PyMuPDF (fitz)
        pdf_document = fitz.open(file_path)  # Open the file using its path
        text = ""

        # Extract text from each page in the PDF
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)  # Load each page by number
            text += page.get_text()  # Extract text from the page

        return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

# Route to display uploaded files
@app.route('/uploads')
def uploaded_files():
    files = File.query.all()  # Get all files from the database
    return render_template('uploads.html', files=files)

# Route to serve the uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file = File.query.filter_by(filename=filename).first_or_404()
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
