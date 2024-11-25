from flask import jsonify, request, send_file,render_template,redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import AI_info,User,File,db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
# jwd authondictions functins:
# from app import allowed_file
from ai_processing.preprocessing_files import load_pdf_doc_split, embadding_and_store,csv_documet_load
from ai_processing.generate_answer_ai import get_result, generate_answer
# Assuming you have a function to fetch file details by filename or index_id
def get_file_details(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        print(file.to_dict())
        return file.to_dict()  # Return file details as dictionary
    return None



def register_routes(app):

    #to get the all users
    @app.route("/users", methods=["GET"])
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
    @app.route("/bot-create", methods=["GET", "POST"])
    @jwt_required()
    def bot_create():
        if request.method == 'POST':
            print("inside")
            # Check if the file is in the request
            if 'file' not in request.files:
                return 'No file part', 400

            file = request.files['file']
            print(file)

            # Check if the filename is empty
            if file.filename == '':
                return 'No selected file', 400

            # Define the allowed file check function
            def allowed_file(filename):
                print(filename)
                print('.' in filename and filename.rsplit('.', 1)[1].lower())
                print('.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

            # If the file is allowed, process it
            if file and allowed_file(file.filename):
                print("check the file extansion")
                filename = secure_filename(file.filename)
                file_type = file.mimetype
                user_id = get_jwt_identity()  # Ensure that user_id is available in the request context

                # Set the upload path
                upload_path = os.path.join(app.config['csv_file'], filename)

                # Ensure the upload folder exists
                if not os.path.exists(app.config['csv_file']):
                    os.makedirs(app.config['csv_file'])

                # Save the file to the specified path
                file.save(upload_path)

                # # Check if the file is empty
                # if os.path.getsize(upload_path) == 0:
                #     return 'Uploaded file is empty. Please upload a valid file.', 400

                print(f"File saved successfully to {upload_path}")

                # If the file is a CSV, process it
                
                print(file_type)
                if file_type == 'text/csv':
                    chunked = csv_documet_load(upload_path)
                    print(f"Extracted chunks: {chunked}")
                    print(f"Number of chunks: {len(chunked)}")

                    # Embedding and storing the file (ensure the function works as expected)
                    embedding_path = embadding_and_store(chuked=chunked, file_name=filename)

                    # Create a new File record and add it to the database
                    new_file = File(
                        filename=filename,
                        file_type=file_type,
                        file_data=file.read(),  # Read the file content (be cautious with large files)
                        index_file_path=embedding_path,
                        user_id=user_id
                    )
                    db.session.add(new_file)
                    db.session.commit()

                    print(f"File record added to database: {new_file}")
                    return "File uploaded successfully", 200

                else:
                    return "Invalid file type. Only CSV files are allowed.", 400

        return "Good request", 200

            # return render_template('upload.html')
    


    @app.route('/chat', methods=['GET', 'POST'])
    @jwt_required()
    def chat():
        if request.method == 'POST':
            print("hello")
            user_id = get_jwt_identity()  # Ensure that user_id is available in the request context

            # Get question from form data; default if not present
            user_question = request.form.get('question', "No question provided")
            print(user_question)
            file_id = request.form.get('file_id')  # Get the file_id from the form or session
            if file_id:
                file_details = get_file_details(file_id)
                print(file_details)

                result_retrive = get_result(path=file_details["index_file_path"], user_question=user_question)
                print(result_retrive)

                responce = generate_answer(result_retrive, user_question)
                print(responce)

                # Create a new File record and add it to the database
                new_file = AI_info(
                    questions=user_question,  # store the question from the user
                    file_id=file_id,  # Read the file content (be cautious with large files)
                    user_id=user_id
                )
                db.session.add(new_file)
                db.session.commit()
                print(f"File record added to database: {new_file}")

                return jsonify({'response': responce})

            else:
                return jsonify({'response': "No file ID provided."})

        return "error", 401