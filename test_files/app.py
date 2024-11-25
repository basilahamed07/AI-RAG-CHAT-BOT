import fitz  # PyMuPDF
import os
from flask import Flask,jsonify, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import time
from preprocessing_files import load_pdf_doc_split,embadding_and_store # Ensure this is your preprocessing module that works
from vector_store import get_result,generate_answer
# Initialize the Flask app and SQLAlchemy e
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost/test_db'  # Database URI
app.config['UPLOAD_FOLDER'] = 'uploads/pdf'  # Folder where uploaded files will be stored
app.config['ALLOWED_EXTENSIONS'] = {'csv'}  # Allowed file extensions
app.secret_key = 'your_secret_key'  # Required for forms (CSRF protection)

db = SQLAlchemy(app)

# File model (already provided in the question)


# class index_data(db.Model):
#     __tablename__ = 'index_data'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     index_file_path = db.Column(db.String(100), unique=True, nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'index_file_path': self.index_file_path,
#             'created_at': self.created_at,
#         }


class File(db.Model):
    __tablename__ = 'file_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    file_type = db.Column(db.String(256), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # index_id = db.Column(db.Integer, db.ForeignKey('index_data.id'), nullable=True)
    index_file_path = db.Column(db.String(100), unique=True, nullable=False)
    # users = db.relationship('index_data', backref=db.backref('index_data', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'created_at': self.created_at,
            "index_file_path": self.index_file_path,
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

            #path update
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(upload_path)  # Save the file to the uploads folder
            
            # Check if the file is actually saved and not empty
            if os.path.getsize(upload_path) == 0:
                return 'Uploaded file is empty. Please upload a valid file.'
            
            print(f"File saved successfully to {upload_path}")

            # Save file metadata to the database
            

            # for load the pdf and chubked the data
            if file_type == 'application/pdf':
                chunked = load_pdf_doc_split(upload_path)
                print(f"Extracted pages: {chunked}")
            print(len(chunked))

            #embadding and store the file
            embadding = embadding_and_store(chuked=chunked,file_name=filename)
            
            new_file = File(filename=filename, file_type=file_type, file_data=file.read(),index_file_path=embadding)
            db.session.add(new_file)
            db.session.commit()
            print(new_file)
            return redirect(url_for('uploaded_files'))
            # r
    return render_template('upload.html')


# Assuming you have a function to fetch file details by filename or index_id
def get_file_details(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        print(file.to_dict())
        return file.to_dict()  # Return file details as dictionary
    return None

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        print("hello")
        # user_message = request.form['user_message']
        # Example: if the user asks for file details or similar commands
        # if 'file details' in user_message.lower():
            # Fetch file details based on some logic (e.g., index_id, file_id, etc.)
        file_id = request.form.get('file_id')  # Get the file_id from the form or session
        file_details = get_file_details(file_id)
        # print(file_details)
        
        result_retrive = get_result(path=file_details["index_file_path"],user_question="Why is Restrict download?")
        print(result_retrive)

        responce = generate_answer(result_retrive,"Why is Restrict download?")
        print(responce)
        # if file_details:
        #     return jsonify({
        #         'response': f"Here are the details of the file: {result_retrive}",
        #         'file_details': result_retrive
        #     })
        # else:
        #     return jsonify({'response': "No file found with that ID."})
        # You can add more conditions to handle other types of queries from the user
        return jsonify({'response': "Sorry, I didn't understand that."})

    return render_template('chat.html')
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
