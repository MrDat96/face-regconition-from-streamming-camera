from flask import request, jsonify, abort, render_template, redirect, Blueprint, flash
from app.models.role import Role
from app.models.user import User
from app.ai_modules.training import training
import os
from threading import Thread
from os import walk

UPLOAD_FOLDER = './data/video'
ALLOWED_EXTENSIONS = set(['mp4', 'mov'])
ENCODE_DIRECTORY_PATH = os.getenv("ENCODE_PATH")
VIDEO_DIRECTORY_STORE_PATH = os.getenv("VIDEO_STORE_PATH")

training_api = Blueprint('training_api', __name__)
# View all role with action
@training_api.route('/training/view_all')
def viewAllUsers(action="view_all", user_id=""):
    # users = User.get_all_with_Role()
    # print(users)
    message=""
    if (action == "view_all"):
        list = []
        f = []
        for (dirpath, dirnames, filenames) in walk(ENCODE_DIRECTORY_PATH):
            f.extend(filenames)
            
        for file_name in f:
            trained_id = get_file_name_only(file_name).upper()
            user = User.getUserById(trained_id)
            list.append((trained_id, user))
        message = ""
        return render_template('view_all_trained.html', page_name="Trained User", list=list, message=message)

# Add a new Role
@training_api.route('/training/add_new', methods=['GET', 'POST'])
def addNewUserWithFace():
    message = ""
    users = User.get_all()
    print(users)
    user_id = None
    if request.method == 'POST':
        try:
            form = request.form
            user_id = form['user_id']
            print(user_id)
            
            if (user_id == ""):
                message = "User ID cannot be empty"

            if (message == ""):
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Save role error! Please try again!'
            return

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            print("No file selected")
            return redirect(request.url)

        print(file.filename)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            path= os.path.join(VIDEO_DIRECTORY_STORE_PATH, file.filename)
            print(path)
            file.save(path)
            flash('Upload successful')
            print("Upload successful")
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            flash('Server processing training')
            input_video_path = path
            if (user_id is not None):
                thread = Thread(target = training, args=(input_video_path,ENCODE_DIRECTORY_PATH,user_id))
                thread.start()
                #result = training(input_video_path, ENCODE_DIRECTORY_PATH, user_id)
            else:
                print("It must stop before this step")
        else:
            flash("File not allow")
            print("File not allow")

    return render_template('training_add_new.html', page_name="Add new training user by id",message=message, users=users)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_name_only(filename):
    return filename.rsplit('.', 1)[0].lower()