from flask import jsonify, request, send_file,render_template,redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import AI_info,User,File,db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
# jwd authondictions functins:
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def register_routes(app):
    #to get the all users
    @app.route("/users", method=["GET"])
    @jwt_required()
    def get_users():
        users = User.query.all()
        return jsonify([trash.to_dict() for trash in users])
    
    #to register the users
    @app.route('/register', methods=['POST'])
    def register_user():

        #get the data from the json  file
        data = request.json
        #check if the data was correct or not
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        #check if the username is present or not
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'User already exists'}), 400
        #create the password in encripted file
        hashed_password = generate_password_hash(data['password'])
        
        # adding the User table for username and password
        new_user = User(username=data['username'], password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
    #login the users
    @app.route('/login', methods=['POST'])
    def login_user():
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'username': user.username,
                'userId': user.id,
            }
        }), 200
    # for creaet the bot for individual files
    @app.route("/bot-create", method=["GET","POST"])
    @jwt_required()
    def bot_create():
        if request.method == 'POST':
            if 'file' not in request.files:
                return jsonify({'error': 'no file part'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'no selected file'}), 401
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_type = file.mimetype
                file = request.files["file"]
                # file_data = file.read()  # Get the file content

                # Save the file to the server
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(upload_path)  # Save the file to the uploads folder

                print(f"File saved successfully to {upload_path}")
                # If the file is a PDF, extract its text using the saved file path
                
                
                # Save file metadata to the database (you can also save extracted text if you want)
                new_file = File(filename=filename, file_type=file_type, file_data=file_data)
                db.session.add(new_file)
                db.session.commit()

                if file_type == 'application/pdf':
                    pdf_text = extract_pdf_text(upload_path)  # Call the function here with file path
                    print(pdf_text)  # For debugging, print the extracted text

                

                return redirect(url_for('uploaded_files'))

        return render_template('upload.html')